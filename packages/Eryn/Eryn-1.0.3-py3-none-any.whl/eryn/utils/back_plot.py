import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib as mpl

mpl.rcParams[
    "text.usetex"
] = False  # TODO: Handle this properly. If left untreated it fails for people who use tex by default
import matplotlib.pyplot as plt
import corner.corner


class PlotContainer:
    """Automatic plotting and diagnostic information

    This class directs creation of plots. It can be used after MCMC
    runs to easily build plots and diagnostic information. It can also
    be used during runs for consistently updating diagnostic information
    about the current run.

    Args:
        fp (str, optional): File name for output pdf. (default: output)
        backend (object, optional): :class:`eryn.backends.Backend` object that
            holds MCMC data. (default: ``None``)
        thin_chain_by_ac(bool, optional): If True, thin the chain by half the minimum
            autocorrelation length and use a burnin of twice the max autocorrelation length.
            (default: ``False``)
        corner_kwargs (dict, optional): Keyword arguments for building corner
            plots. This can add extra key-value pairs or overwrite defaults.
            Defaults can be found with ``PlotContainer().default_corner_kwargs``.
        parameter_transforms (object, optional): :class:`eryn.utils.TransformContainer`
            object used to convert parameters to desired values for plotting.
            (default: ``None``)
        info_keys (list, optional): List of ``str`` indicating which keys from
            the information dictionary provided by the backend are of interest
            for diagnostics. (default: ``None``)
        which_plots (list, optional): List of ``str``indicating which plot generating
            functions to use. Options are the associated class methods that start
            with ``generate``. (default: ``["info_page", "corner"]``)

    """

    def __init__(
        self,
        fp="output",
        backend=None,
        thin_chain_by_ac=False,
        corner_kwargs={},
        parameter_transforms=None,
        info_keys=None,
        which_plots=["info_page", "corner"],
    ):

        self.backend = backend
        self.fp = fp
        self.thin_chain_by_ac = thin_chain_by_ac

        if parameter_transforms is not None and not isinstance(
            parameter_transforms, TransformContainer
        ):
            raise ValueError(
                "If using parameter_transforms, must be eryn.utils.TransformContainer object."
            )
        self.parameter_transforms = parameter_transforms
        self.corner_kwargs = corner_kwargs

        self.injection = self.backend.truth
        if self.injection is not None and len(self.injection) == 0:
            self.injection = None

        for key, default in self.default_corner_kwargs.items():
            self.corner_kwargs[key] = self.corner_kwargs.get(key, default)

        self.info_keys = info_keys
        self.which_plots = which_plots

    def transform(self, info):
        """Transform the samples in the infromation dictionary

        Args:
            info (dict): Information dictionary from the backend.

        """
        if self.parameter_transforms is not None:
            info["samples"] = self.parameter_transforms(info["samples"])
        return info

    @property
    def default_corner_kwargs(self):
        default_corner_kwargs = dict(
            levels=(1 - np.exp(-0.5 * np.array([1, 2, 3]) ** 2)),
            figsize=(18, 18),
            bins=25,
            plot_density=False,
            plot_datapoints=False,
            smooth=0.4,
            labels=None,
            fill_contours=True,
            # contour_kwargs={"colors": "blue"},
            hist_kwargs={"density": True},
            truths=self.injection,
            show_titles=True,
            title_fmt=".2e",
        )
        return default_corner_kwargs

    @property
    def info_keys(self):
        return self._info_keys

    @info_keys.setter
    def info_keys(self, info_keys):
        if info_keys is not None:
            if not isinstance(info_keys, list):
                raise ValueError("info_keys must be a list.")

            self._info_keys = info_keys

        else:
            self._info_keys = [
                "ntemps",
                "nwalkers",
                "nbranches",
                "max logl",
                "shapes",
            ]

    def add_backend(self, backend, custom_backend=False):
        """Add a backend after initialization

        Args:
            backend (object): Either a :class:`eryn.backends.Backend`
                or :class:`eryn.backends.HDFBackend` object or a custom backend
                object.
            custom_backend (bool, optional): If using a custom backend class,
                this should be True. (default: ``False``)

        """
        # custom_backend is if they make their own
        if (
            not isinstance(backend, Backend) and not isinstance(backend, HDFBackend)
        ) and not custom_backend:
            raise ValueError("Backend must be a default backend")

        self.backend = backend

    def generate_corner(
        self, burn=0, thin=1, pdf=None, name=None, info=None, **corner_kwargs
    ):
        """Build a corner plot

        This function builds a corner plot to be added to a pdf.

        Args:
            burn (int, optional): Number of samples to burn. If
                ``self.thin_chain_by_ac == True``, then this is overridden.
                (default: ``0``)
            thin (int, optional): Number of samples to burn. If
                ``self.thin_chain_by_ac == True``, then this is overridden.
                (default: ``1``)
            pdf (object, optional): An open PdfPages object
                (`see her for an example <https://matplotlib.org/stable/gallery/misc/multipage_pdf.html>`_).
                It will not be closed by this function. If not provided, a new pdf
                will be opened, added to, then closed.
                (default: ``None``)
            name (str, optional): If not providing ``pdf`` kwarg, ``name`` will be
                the name of the pdf document that is created and saved.
                (default: ``None``)
            info (dict, optional): Information dictionary from the backend. If not
                provided, it will be retrieved from the backend.
                (default: ``None``)
            corner_kwargs (dict, optional): Pass kwarg arguments direct to
                the corner plot. This will temperorarily overwrite entries in
                the ``self.corner_kwargs`` attribute.


        """
        # get info from backend
        if info is None and self.backend is not None:
            info = self.transform(self.backend.get_info(discard=burn, thin=thin))

        elif info is None:
            raise ValueError("Need to provide either info or self.backend.")

        if self.thin_chain_by_ac:
            burn = info["ac_burn"]
            thin = info["ac_thin"]

        # build corner_kwargs with self.corner_kwargs
        for key, val in self.corner_kwargs.items():
            corner_kwargs[key] = corner_kwargs.get(key, val)

        # adjust color info # TODO: This is bypasssed by adding colormap according to temperature
        if "hist_kwargs" in corner_kwargs:
            if "color" in corner_kwargs["hist_kwargs"] and "color" in corner_kwargs:
                corner_kwargs["hist_kwargs"]["color"] = corner_kwargs["color"]

        # open new pdf if not provided
        if pdf is None:
            close_file = True
            name = self.fp if name is None else name
            pdf = PdfPages(name + "_corner.pdf")
        else:
            close_file = False

        # make corner plot for each temperature
        # NOTE: I am now flattenimg the chains across walkers. Probably we need to think carefully here
        for key, coords in info["samples"].items():
            nsteps, ntemps, nwalkers, nleaves_max, ndim = coords.shape
            clrs = plt.cm.viridis(np.linspace(0, 1, ntemps))  # Get a set of colors
            for temp in range(ntemps):

                naninds = np.logical_not(np.isnan(coords[:, temp, :, :, 0].flatten()))
                samples_in = np.zeros(
                    (coords[:, temp, :, :, 0].flatten()[naninds].shape[0], ndim)
                )  # init the chains to plot

                # get the samples to plot
                for d in range(ndim):
                    givenparam = coords[:, temp, :, :, d].flatten()
                    samples_in[:, d] = givenparam[
                        np.logical_not(np.isnan(givenparam))
                    ]  # Discard the NaNs, each time they change the shape of the samples_in

                # Build corner figure. Wrapping around a try-except in order to let it finish plotting the "healthy" chains
                try:
                    fig = plt.figure(figsize=corner_kwargs["figsize"])
                    corner_kwargs["fig"] = fig  # handling the figure size properly
                    corner_kwargs["color"] = clrs[temp]  # Adding the color
                    fig = corner.corner(samples_in, **corner_kwargs,)

                    # add informational title
                    fig.suptitle(
                        f"Branch: {key}\nTemperature: {temp}\nSample Size: {samples_in.shape[0]}"
                    )
                    # save to open pdf
                    pdf.savefig(fig)
                    # close the plot not the pdf
                    plt.close()
                except Exception as e:
                    print(
                        f" Did not manage to make the corner plot for Branch: {key}, Temperature: {temp}.\nActual error: [{e}]"
                    )

        # if pdf was created here, close it
        if close_file:
            pdf.close()

    def generate_parameter_chains(
        self, burn=0, thin=1, pdf=None, name=None, labels=None, info=None
    ):
        """Generate plots of the chains of the cold chain.

        This function builds plots of the MCMC traces to be added to a pdf.

        Args:
            burn (int, optional): Number of samples to burn. If
                ``self.thin_chain_by_ac == True``, then this is overridden.
                (default: ``0``)
            thin (int, optional): Number of samples to burn. If
                ``self.thin_chain_by_ac == True``, then this is overridden.
                (default: ``1``)
            pdf (object, optional): An open PdfPages object
                (`see her for an example <https://matplotlib.org/stable/gallery/misc/multipage_pdf.html>`_).
                It will not be closed by this function. If not provided, a new pdf
                will be opened, added to, then closed.
                (default: ``None``)
            name (str, optional): If not providing ``pdf`` kwarg, ``name`` will be
                the name of the pdf document that is created and saved.
                (default: ``None``)
            labels (str, opitional): A list of the parameter names to be shown
                as the y-labes of the trace plots.
            info (dict, optional): Information dictionary from the backend. If not
                provided, it will be retrieved from the backend.
                (default: ``None``)
        """
        # get info from backend
        if info is None and self.backend is not None:
            info = self.transform(self.backend.get_info(discard=burn, thin=thin))

        elif info is None:
            raise ValueError("Need to provide either info or self.backend.")

        if self.thin_chain_by_ac:
            burn = info["ac_burn"]
            thin = info["ac_thin"]

        # open new pdf if not provided
        if pdf is None:
            close_file = True
            name = self.fp if name is None else name
            pdf = PdfPages(name + "_traces.pdf")
        else:
            close_file = False

        # make a trace plot for each temperature
        for key, coords in info["samples"].items():
            nsteps, ntemps, nwalkers, nleaves_max, ndim = coords.shape
            temp = 0

            samples_in = np.zeros(
                (coords[:, temp, :, :, 0].flatten().shape[0], ndim)
            )  # init the chains to plot
            fig, ax = plt.subplots(ndim, 1, sharex=True, figsize=(12, 6))
            fig.subplots_adjust(hspace=0)  # No space between subplots

            # get the samples to plot
            for d in range(ndim):
                samples_in[:, d] = coords[:, temp, :, :, d].flatten()
                # Build the figure.
                ax[d].scatter(
                    np.arange(0, samples_in[:, d].shape[0]),
                    samples_in[:, d],
                    marker=".",
                    s=2.0,
                    color="k",
                    alpha=0.4,
                )
                if labels is not None:
                    ax[d].set_ylabel(labels[d])
            ax[-1].set_xlim(0, samples_in.shape[0])
            ax[-1].set_xlabel("Samples")

            # add informational title
            fig.suptitle(f"Branch: {key}\nTemperature: {temp}")
            # save to open pdf
            pdf.savefig(fig)
            # close the plot not the pdf
            plt.close()

        # if pdf was created here, close it
        if close_file:
            pdf.close()

    def generate_parameter_chains_per_temperature(
        self, burn=0, thin=1, pdf=None, name=None, labels=None, info=None
    ):
        """Generate plots of the chains per temperature.

        This function builds plots of the MCMC traces to be added to a pdf.

        Args:
            burn (int, optional): Number of samples to burn. If
                ``self.thin_chain_by_ac == True``, then this is overridden.
                (default: ``0``)
            thin (int, optional): Number of samples to burn. If
                ``self.thin_chain_by_ac == True``, then this is overridden.
                (default: ``1``)
            pdf (object, optional): An open PdfPages object
                (`see her for an example <https://matplotlib.org/stable/gallery/misc/multipage_pdf.html>`_).
                It will not be closed by this function. If not provided, a new pdf
                will be opened, added to, then closed.
                (default: ``None``)
            name (str, optional): If not providing ``pdf`` kwarg, ``name`` will be
                the name of the pdf document that is created and saved.
                (default: ``None``)
            labels (str, opitional): A list of the parameter names to be shown
                as the y-labes of the trace plots.
            info (dict, optional): Information dictionary from the backend. If not
                provided, it will be retrieved from the backend.
                (default: ``None``)

        """
        # get info from backend
        if info is None and self.backend is not None:
            info = self.transform(self.backend.get_info(discard=burn, thin=thin))

        elif info is None:
            raise ValueError("Need to provide either info or self.backend.")

        if self.thin_chain_by_ac:
            burn = info["ac_burn"]
            thin = info["ac_thin"]

        # open new pdf if not provided
        if pdf is None:
            close_file = True
            name = self.fp if name is None else name
            pdf = PdfPages(name + "_traces_param_temp.pdf")
        else:
            close_file = False

        # make a trace plot for each temperature
        for key, coords in info["samples"].items():
            nsteps, ntemps, nwalkers, nleaves_max, ndim = coords.shape
            # Define a colormap
            clrs = plt.cm.viridis(np.linspace(0, 1, ntemps))
            for temp in range(ntemps):

                samples_in = np.zeros(
                    (coords[:, temp, :, :, 0].flatten().shape[0], ndim)
                )  # init the chains to plot
                fig, ax = plt.subplots(ndim, 1, sharex=True, figsize=(12, 6))
                fig.subplots_adjust(hspace=0)  # No space between subplots

                # get the samples to plot
                for d in range(ndim):
                    samples_in[:, d] = coords[:, temp, :, :, d].flatten()
                    # Build the figure.
                    ax[d].scatter(
                        np.arange(0, samples_in[:, d].shape[0]),
                        samples_in[:, d],
                        marker=".",
                        s=2.0,
                        color=clrs[temp],
                        alpha=0.5,
                    )
                    if labels is not None:
                        ax[d].set_ylabel(labels[d])
                ax[-1].set_xlim(0, samples_in.shape[0])
                ax[-1].set_xlabel("Samples")

                # add informational title
                fig.suptitle(f"Branch: {key}\nTemperature: {temp}")
                # save to open pdf
                pdf.savefig(fig)
                # close the plot not the pdf
                plt.close()

        # if pdf was created here, close it
        if close_file:
            pdf.close()

    def generate_parameter_chains_per_temperature_per_walker(
        self, burn=0, thin=1, pdf=None, name=None, labels=None, info=None
    ):
        """Generate plots of the chains per temperature per walker.

        This function builds plots of the MCMC traces to be added to a pdf.

        Args:
            burn (int, optional): Number of samples to burn. If
                ``self.thin_chain_by_ac == True``, then this is overridden.
                (default: ``0``)
            thin (int, optional): Number of samples to burn. If
                ``self.thin_chain_by_ac == True``, then this is overridden.
                (default: ``1``)
            pdf (object, optional): An open PdfPages object
                (`see her for an example <https://matplotlib.org/stable/gallery/misc/multipage_pdf.html>`_).
                It will not be closed by this function. If not provided, a new pdf
                will be opened, added to, then closed.
                (default: ``None``)
            name (str, optional): If not providing ``pdf`` kwarg, ``name`` will be
                the name of the pdf document that is created and saved.
                (default: ``None``)
            labels (str, opitional): A list of the parameter names to be shown
                as the y-labes of the trace plots.
            info (dict, optional): Information dictionary from the backend. If not
                provided, it will be retrieved from the backend.
                (default: ``None``)


        """
        # get info from backend
        if info is None and self.backend is not None:
            info = self.transform(self.backend.get_info(discard=burn, thin=thin))

        elif info is None:
            raise ValueError("Need to provide either info or self.backend.")

        if self.thin_chain_by_ac:
            burn = info["ac_burn"]
            thin = info["ac_thin"]

        # open new pdf if not provided
        if pdf is None:
            close_file = True
            name = self.fp if name is None else name
            pdf = PdfPages(name + "_traces_param_temp_walker.pdf")
        else:
            close_file = False

        # make a trace plot for each temperature
        for key, coords in info["samples"].items():
            nsteps, ntemps, nwalkers, nleaves_max, ndim = coords.shape
            # Define a colormap
            clrs = plt.cm.viridis(np.linspace(0, 1, ntemps))
            for temp in range(ntemps):

                fig, ax = plt.subplots(ndim, 1, sharex=True, figsize=(12, 6))
                fig.subplots_adjust(hspace=0)  # No space between subplots

                # get the samples to plot
                for d in range(ndim):
                    for w in range(nwalkers):
                        chain = coords[:, temp, w, :, d]
                        # Build the figure.
                        ax[d].plot(
                            np.arange(0, chain.shape[0]),
                            chain,
                            color=clrs[temp],
                            alpha=0.1,
                        )
                    if labels is not None:
                        ax[d].set_ylabel(labels[d])
                ax[-1].set_xlim(0, chain.shape[0])
                ax[-1].set_xlabel("Samples")

                # add informational title
                fig.suptitle(f"Branch: {key}\nTemperature: {temp}")
                # save to open pdf
                pdf.savefig(fig)
                # close the plot not the pdf
                plt.close()

        # if pdf was created here, close it
        if close_file:
            pdf.close()

    def generate_posterior_chains(self, burn=0, thin=1, pdf=None, name=None, info=None):
        """Generate plots of the posterior chains per temperature.

        This function builds plots of the MCMC traces to be added to a pdf.

        Args:
            burn (int, optional): Number of samples to burn. If
                ``self.thin_chain_by_ac == True``, then this is overridden.
                (default: ``0``)
            thin (int, optional): Number of samples to burn. If
                ``self.thin_chain_by_ac == True``, then this is overridden.
                (default: ``1``)
            pdf (object, optional): An open PdfPages object
                (`see her for an example <https://matplotlib.org/stable/gallery/misc/multipage_pdf.html>`_).
                It will not be closed by this function. If not provided, a new pdf
                will be opened, added to, then closed.
                (default: ``None``)
            name (str, optional): If not providing ``pdf`` kwarg, ``name`` will be
                the name of the pdf document that is created and saved.
                (default: ``None``)
            info (dict, optional): Information dictionary from the backend. If not
                provided, it will be retrieved from the backend.
                (default: ``None``)

        """
        # get info from backend
        if info is None and self.backend is not None:
            info = self.transform(self.backend.get_info(discard=burn, thin=thin))

        elif info is None:
            raise ValueError("Need to provide either info or self.backend.")

        if self.thin_chain_by_ac:
            burn = info["ac_burn"]
            thin = info["ac_thin"]

        # open new pdf if not provided
        if pdf is None:
            close_file = True
            name = self.fp if name is None else name
            pdf = PdfPages(name + "_traces_post.pdf")
        else:
            close_file = False

        # make a trace plot for each temperature
        ntemps = info["log_prob"].shape[1]
        # Define a colormap
        clrs = plt.cm.viridis(np.linspace(0, 1, ntemps))
        for temp in range(ntemps):
            # get the samples to plot
            post = info["log_prob"][:, temp, :].flatten()
            # Build the figure.
            fig = plt.figure(figsize=(12, 6))
            plt.scatter(
                np.arange(0, post.shape[0]),
                post,
                marker=".",
                s=2.0,
                color=clrs[temp],
                alpha=0.5,
            )
            plt.ylabel(f"$p:T{temp}$")
            plt.xlim(0, post.shape[0])
            plt.xlabel("Samples")

            # save to open pdf
            pdf.savefig(fig)

        # close the plot not the pdf
        plt.close()

        # if pdf was created here, close it
        if close_file:
            pdf.close()

    def generate_temperature_chains(
        self, thin=1, pdf=None, name=None, info=None, onefig=True
    ):
        """Generate plots of the temperature chains.

        This function builds plots of the MCMC traces to be added to a pdf.

        Args:
            burn (int, optional): Number of samples to burn. If
                ``self.thin_chain_by_ac == True``, then this is overridden.
                (default: ``0``)
            thin (int, optional): Number of samples to burn. If
                ``self.thin_chain_by_ac == True``, then this is overridden.
                (default: ``1``)
            pdf (object, optional): An open PdfPages object
                (`see her for an example <https://matplotlib.org/stable/gallery/misc/multipage_pdf.html>`_).
                It will not be closed by this function. If not provided, a new pdf
                will be opened, added to, then closed.
                (default: ``None``)
            name (str, optional): If not providing ``pdf`` kwarg, ``name`` will be
                the name of the pdf document that is created and saved.
                (default: ``None``)
            info (dict, optional): Information dictionary from the backend. If not
                provided, it will be retrieved from the backend.
                (default: ``None``)
            onefig (bool, optional): Flag to plot all chains in one figure
                (default: ``False``)
        """
        # get info from backend
        if info is None and self.backend is not None:
            info = self.transform(
                self.backend.get_info(discard=0, thin=thin)
            )  # NOTE: Here we want to see how the temperatures adjust, thus discard=1

        elif info is None:
            raise ValueError("Need to provide either info or self.backend.")

        if self.thin_chain_by_ac:
            thin = info["ac_thin"]

        # open new pdf if not provided
        if pdf is None:
            close_file = True
            name = self.fp if name is None else name
            pdf = PdfPages(name + "_traces_temps.pdf")
        else:
            close_file = False

        # make a trace plot for each temperature
        ntemps = info["betas"].shape[1]
        # Define a colormap
        clrs = plt.cm.viridis(np.linspace(0, 1, ntemps))

        if onefig:
            fig = plt.figure(figsize=(12, 6))
            plt.ylabel(r"$\beta$")
            plt.xlabel("Samples")

        # Loop over the temperatures
        for temp in range(1, ntemps - 1):
            # get the samples to plot
            betas = info["betas"][:, temp].flatten()
            # Build the figure.
            if onefig:
                plt.plot(
                    np.arange(0, betas.shape[0]),
                    betas,
                    color=clrs[temp],
                    alpha=0.9,
                    label=r"$\beta_{{{}}}$".format(temp),
                )
                plt.xlim(0, betas.shape[0])
            else:
                fig = plt.figure(figsize=(12, 6))
                plt.plot(
                    np.arange(0, betas.shape[0]), betas, color=clrs[temp], alpha=0.9
                )
                plt.ylabel(r"$\beta_{{{}}}$".format(temp))
                plt.xlim(0, betas.shape[0])
                plt.xlabel("Samples")
                # save to open pdf
                pdf.savefig(fig)

        if onefig:
            # save to open pdf in case we want a single figure
            pdf.savefig(fig)

        # close the plot not the pdf
        plt.close()

        # if pdf was created here, close it
        if close_file:
            pdf.close()

    def generate_leaves_chains(
        self, burn=0, thin=1, pdf=None, name=None, labels=None, info=None
    ):
        """Generate plots of the chains per leaf for the cold chain.

        This function builds plots of the MCMC traces to be added to a pdf.

        Args:
            burn (int, optional): Number of samples to burn. If
                ``self.thin_chain_by_ac == True``, then this is overridden.
                (default: ``0``)
            thin (int, optional): Number of samples to burn. If
                ``self.thin_chain_by_ac == True``, then this is overridden.
                (default: ``1``)
            pdf (object, optional): An open PdfPages object
                (`see her for an example <https://matplotlib.org/stable/gallery/misc/multipage_pdf.html>`_).
                It will not be closed by this function. If not provided, a new pdf
                will be opened, added to, then closed.
                (default: ``None``)
            name (str, optional): If not providing ``pdf`` kwarg, ``name`` will be
                the name of the pdf document that is created and saved.
                (default: ``None``)
            labels (str, opitional): A list of the parameter names to be shown
                as the y-labes of the trace plots.
            info (dict, optional): Information dictionary from the backend. If not
                provided, it will be retrieved from the backend.
                (default: ``None``)

        """
        # get info from backend
        if info is None and self.backend is not None:
            info = self.transform(self.backend.get_info(discard=burn, thin=thin))

        elif info is None:
            raise ValueError("Need to provide either info or self.backend.")

        if self.thin_chain_by_ac:
            burn = info["ac_burn"]
            thin = info["ac_thin"]

        # open new pdf if not provided
        if pdf is None:
            close_file = True
            name = self.fp if name is None else name
            pdf = PdfPages(name + "_traces_param_leaves.pdf")
        else:
            close_file = False

        # make a trace plot for each temperature
        for key, coords in info["samples"].items():
            nsteps, ntemps, nwalkers, nleaves_max, ndim = coords.shape
            # Define a colormap
            clrs = plt.cm.viridis(np.linspace(0, 1, ntemps))
            temp = 0  # Plot only the cold chain
            for leaf in range(nleaves_max):

                samples_in = np.zeros(
                    (coords[:, temp, :, leaf, 0].flatten().shape[0], ndim)
                )  # init the chains to plot
                fig, ax = plt.subplots(ndim, 1, sharex=True, figsize=(12, 6))
                fig.subplots_adjust(hspace=0)  # No space between subplots

                # get the samples to plot
                for d in range(ndim):
                    samples_in[:, d] = coords[:, temp, :, leaf, d].flatten()
                    # Build the figure.
                    ax[d].scatter(
                        np.arange(0, samples_in[:, d].shape[0]),
                        samples_in[:, d],
                        marker=".",
                        s=2.0,
                        color=clrs[temp],
                        alpha=0.5,
                    )
                    if labels is not None:
                        ax[d].set_ylabel(labels[d])
                ax[-1].set_xlim(0, samples_in.shape[0])
                ax[-1].set_xlabel("Samples")

                # add informational title
                fig.suptitle(f"Branch: {key}\nTemperature: {temp}, Leaf: {leaf}")
                # save to open pdf
                pdf.savefig(fig)
                # close the plot not the pdf
                plt.close()

        # if pdf was created here, close it
        if close_file:
            pdf.close()

    def generate_k_per_temperature_chains(self, thin=1, pdf=None, name=None, info=None):
        """Generate plots of the k chains.

        This function builds plots of the MCMC traces to be added to a pdf.

        Args:
            burn (int, optional): Number of samples to burn. If
                ``self.thin_chain_by_ac == True``, then this is overridden.
                (default: ``0``)
            thin (int, optional): Number of samples to burn. If
                ``self.thin_chain_by_ac == True``, then this is overridden.
                (default: ``1``)
            pdf (object, optional): An open PdfPages object
                (`see her for an example <https://matplotlib.org/stable/gallery/misc/multipage_pdf.html>`_).
                It will not be closed by this function. If not provided, a new pdf
                will be opened, added to, then closed.
                (default: ``None``)
            name (str, optional): If not providing ``pdf`` kwarg, ``name`` will be
                the name of the pdf document that is created and saved.
                (default: ``None``)
            info (dict, optional): Information dictionary from the backend. If not
                provided, it will be retrieved from the backend.
                (default: ``None``)

        """
        # get info from backend
        if info is None and self.backend is not None:
            info = self.transform(
                self.backend.get_info(discard=0, thin=thin)
            )  # NOTE: Here we want to see how the temperatures adjust, thus discard=1

        elif info is None:
            raise ValueError("Need to provide either info or self.backend.")

        if self.thin_chain_by_ac:
            thin = info["ac_thin"]

        # open new pdf if not provided
        if pdf is None:
            close_file = True
            name = self.fp if name is None else name
            pdf = PdfPages(name + "_traces_k.pdf")
        else:
            close_file = False

        inds = self.backend.get_value("inds")  # Get the leaves out
        branches = {name: np.sum(inds[name], axis=-1, dtype=int) for name in inds}
        nbrsmx = max(
            self.backend.nleaves_max
        )  # Maximum number of branches across the forest
        bns = (
            np.arange(1, nbrsmx + 2) - 0.5
        )  # Get maximum allowed number of leaves for the given branch

        # make a trace plot for each temperature
        ntemps = info["betas"].shape[1]
        clrs = plt.cm.viridis(np.linspace(0, 1, ntemps))  # Define a colormap

        for temp in range(0, ntemps):

            fig = plt.figure(figsize=(8, 6))
            for (
                branch
            ) in (
                branches
            ):  # Get the total number of components/branches per temperature
                if branch == list(branches.keys())[0]:
                    k_chain = branches[branch][:, temp].flatten()
                else:
                    k_chain += branches[branch][:, temp].flatten()

            plt.hist(
                k_chain,
                bins=bns,
                color=clrs[temp],
                edgecolor=clrs[temp],
                alpha=0.4,
                lw=3,
                density=True,
            )
            plt.xticks(np.arange(1, nbrsmx + 1))
            plt.xlabel(r"$\#$ of Branches in the data")
            # add informational title
            fig.suptitle(f"\nTemperature: {temp}")
            # save to open pdf
            pdf.savefig(fig)

        # close the plot not the pdf
        plt.close()

        # if pdf was created here, close it
        if close_file:
            pdf.close()

    def generate_k_per_tree_chains(self, thin=1, pdf=None, name=None, info=None):
        """Generate plots of the k chains per type of model.

        This function builds plots of the MCMC traces to be added to a pdf.

        Args:
            burn (int, optional): Number of samples to burn. If
                ``self.thin_chain_by_ac == True``, then this is overridden.
                (default: ``0``)
            thin (int, optional): Number of samples to burn. If
                ``self.thin_chain_by_ac == True``, then this is overridden.
                (default: ``1``)
            pdf (object, optional): An open PdfPages object
                (`see her for an example <https://matplotlib.org/stable/gallery/misc/multipage_pdf.html>`_).
                It will not be closed by this function. If not provided, a new pdf
                will be opened, added to, then closed.
                (default: ``None``)
            name (str, optional): If not providing ``pdf`` kwarg, ``name`` will be
                the name of the pdf document that is created and saved.
                (default: ``None``)
            info (dict, optional): Information dictionary from the backend. If not
                provided, it will be retrieved from the backend.
                (default: ``None``)

        """
        # get info from backend
        if info is None and self.backend is not None:
            info = self.transform(
                self.backend.get_info(discard=0, thin=thin)
            )  # NOTE: Here we want to see how the temperatures adjust, thus discard=1

        elif info is None:
            raise ValueError("Need to provide either info or self.backend.")

        if self.thin_chain_by_ac:
            thin = info["ac_thin"]

        # open new pdf if not provided
        if pdf is None:
            close_file = True
            name = self.fp if name is None else name
            pdf = PdfPages(name + "_traces_k_per_tree.pdf")
        else:
            close_file = False

        inds = self.backend.get_value("inds")  # Get the leaves out
        branches = {name: np.sum(inds[name], axis=-1, dtype=int) for name in inds}
        nbrsmx = max(
            self.backend.nleaves_max
        )  # Maximum number of branches across the forest
        bns = np.arange(1, nbrsmx + 2) - 0.5  # Get maximum allowed number of leaves
        nmodels = len(list(branches.keys()))

        # make a trace plot for each temperature
        ntemps = info["betas"].shape[1]
        clrs = plt.cm.viridis(np.linspace(0, 1, nmodels))  # Define a colormap

        for temp in range(0, ntemps):

            fig = plt.figure(figsize=(8, 6))
            cntr = 0
            for (
                branch
            ) in (
                branches
            ):  # Get the total number of components/branches per temperature
                k_chain = branches[branch][:, temp].flatten()
                plt.hist(
                    k_chain,
                    bins=bns,
                    color=clrs[cntr],
                    edgecolor=clrs[cntr],
                    histtype="step",
                    alpha=0.9,
                    lw=3,
                    density=True,
                    label=branch,
                )
                cntr += 1

            plt.xticks(np.arange(1, nbrsmx + 1))
            plt.xlabel(r"$\#$ of Branches in the data")
            plt.legend(loc="upper right")
            # add informational title
            fig.suptitle(f"\nTemperature: {temp}")
            # save to open pdf
            pdf.savefig(fig)

        # close the plot not the pdf
        plt.close()

        # if pdf was created here, close it
        if close_file:
            pdf.close()

    def generate_info_page(self, burn=0, thin=1, pdf=None, name=None, info=None):
        """Build an info page

        This function puts an info page in a pdf.

        Args:
            burn (int, optional): Number of samples to burn. If
                ``self.thin_chain_by_ac == True``, then this is overridden.
                (default: ``0``)
            thin (int, optional): Number of samples to burn. If
                ``self.thin_chain_by_ac == True``, then this is overridden.
                (default: ``1``)
            pdf (object, optional): An open PdfPages object
                (`see her for an example <https://matplotlib.org/stable/gallery/misc/multipage_pdf.html>`_).
                It will not be closed by this function. If not provided, a new pdf
                will be opened, added to, then closed.
                (default: ``None``)
            name (str, optional): If not providing ``pdf`` kwarg, ``name`` will be
                the name of the pdf document that is created and saved.
                (default: ``None``)
            info (dict, optional): Information dictionary from the backend. If not
                provided, it will be retrieved from the backend.
                (default: ``None``)

        """
        # get information from backend
        if info is None and self.backend is not None:
            info = self.transform(self.backend.get_info(discard=burn, thin=thin))

        elif info is None:
            raise ValueError("Need to provide either info or self.backend.")

        # build info from long string
        title_str = self.fp + " informat:\n"

        for key in self.info_keys:

            if key not in ["shapes", "max logl"]:
                title_str += f"{key}: {info[key]}\n"

            elif key == "max logl":
                title_str += f"{key}: {info['log_prob'].max()}\n"

            elif key == "shapes":
                for key, shape in info["shapes"].items():
                    title_str += f"{key}:\n"
                    title_str += f"    shape: {shape}\n"
                    title_str += f"    nleaves max: {shape[2]}\n"
                    title_str += f"    ndim: {shape[3]}\n"

        fig = plt.Figure()
        fig.suptitle(title_str, fontsize=16, ha="left", x=0.25)

        # open pdf if not given
        if pdf is None:
            close_file = True
            name = self.fp if name is None else name
            pdf = PdfPages(name + ".pdf")
        else:
            close_file = False

        pdf.savefig(fig)

        plt.close()
        # close file if created here
        if close_file:
            pdf.close()

    def generate_plot_info(self, burn=0, thin=1, pdf=None, name=None, info=None):
        """Build an info page

        This function puts an info page in a pdf.

        Args:
            burn (int, optional): Number of samples to burn. If
                ``self.thin_chain_by_ac == True``, then this is overridden.
                (default: ``0``)
            thin (int, optional): Number of samples to burn. If
                ``self.thin_chain_by_ac == True``, then this is overridden.
                (default: ``1``)
            pdf (object, optional): An open PdfPages object
                (`see her for an example <https://matplotlib.org/stable/gallery/misc/multipage_pdf.html>`_).
                It will not be closed by this function. If not provided, a new pdf
                will be opened, added to, then closed.
                (default: ``None``)
            name (str, optional): If not providing ``pdf`` kwarg, ``name`` will be
                the name of the pdf document that is created and saved.
                (default: ``None``)
            info (dict, optional): Information dictionary from the backend. If not
                provided, it will be retrieved from the backend.
                (default: ``None``)

        """
        # must have backend in this case
        if info is None:
            info = self.transform(self.backend.get_info(discard=burn, thin=thin))

        if pdf is None:
            close_file = True
            name = self.fp if name is None else name
            pdf = PdfPages(name + ".pdf")
        else:
            close_file = False

        # TODO: We will probably need to save to PNG. The PDFs are too heavy for large data
        # TODO: add options

        for plot_i in self.which_plots:
            getattr(self, "generate_" + plot_i)(info=info, pdf=pdf)

        # self.generate_xchange_acceptance_rate(info=info, pdf=pdf)

        # close file if created here
        if close_file:
            pdf.close()


if __name__ == "__main__":
    plot = PlotContainer("../GPU4GW/MBH_for_corner.h5", "mbh")

    plot.generate_corner()
