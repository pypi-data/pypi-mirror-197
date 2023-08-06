import zfit
import matplotlib.pyplot as plt
import alexPlot.funcs.useful_functions as uf
import alexPlot.funcs.plot_functions as pf
import alexPlot.funcs.pulls as pull_funcs
import alexPlot.funcs.axes as axes
import numpy as np
import mplhep
mplhep.style.use('LHCb2')
import matplotlib as mpl

def get_axes(option):
	options = ['pulls', 'pulls_large']
	if option == 'pulls':
		ax_plot, ax_pulls = axes.get_ax_1D_with_pulls()
		return ax_plot, ax_pulls
	elif option == 'pulls_large':
		ax_plot, ax_pulls = axes.get_ax_1D_with_pulls_large()
		return ax_plot, ax_pulls
	else:
		print(f'{option} not in list of options')
		print(options)
		quit()

def plot_data(data_list, filename='plot.pdf', axis='x', log=False, xlabel=None, ylabel=None, ymin=None, ymax=None,
	      		xmin=None, xmax=None, bins=50,
				extra_pyplot_commands=None, also_plot_hist=False, only_canvas=False, label=None, 
				color=None, density=False, units=None, weights=None, legend_title=None,
				figure_title=None, as_subplot=False):

	mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=["k", "#6666ff", "#33cc33", "#ff6666", "#cc66ff", "#993333", "#ff6699", "#8c8c8c", "#999900", "#00cccc"]) 

	if as_subplot:
		only_canvas = True

	if not isinstance(data_list, list):
		data_list = [data_list]
	if weights is not None and not isinstance(weights, list):
		weights_list = [weights]
	else:
		weights_list = weights
	if weights_list is not None and len(data_list) != len(weights_list):
		raise Exception("Number of data items must equal the number of weight items...")

	if not isinstance(color, list):
		color = [color]
	if not isinstance(label, list):
		label = [label]

	N_data = len(data_list)

	plotting_information = uf.get_empty_plotting_information(xlabel, ylabel, ymin, ymax, xmin, xmax)

	if not isinstance(data_list[0], zfit.Data):
		try:
			data_list = uf.convert_to_zfitData(data_list, weights_list)
		except:
			raise Exception("data items need to all be zfit.Data objects, or all numpy arrays...")

	obs, limits = uf.get_range([data_list], plotting_information)

	for index in range(N_data):

		plotting_information[f'obj_{index}'] = {}
		
		plotting_information[f'obj_{index}']['data'] = data_list[index]

		try: plotting_information[f'obj_{index}']['label'] = label[index]
		except: plotting_information[f'obj_{index}']['label'] = None

		try: plotting_information[f'obj_{index}']['c'] = color[index]
		except: plotting_information[f'obj_{index}']['c'] = color[0]


	if not only_canvas: fig = plt.figure(figsize=(13,10))
	if not as_subplot:
		ax_plot = axes.get_ax_1D()
		ax_plot.set_xlim(limits[0], limits[1])
	else:
		ax_plot = plt.gca()
		
	data_points = []
	for key in plotting_information.keys():
		if "obj_" not in key: continue
		info = plotting_information[key]
		
		x_points, y_points, yerr_points, x_range_hist, normalisation = uf.plot_x_y_yerr(info['data'], ax=ax_plot, bins=bins, axis=axis, 
										  					also_plot_hist=also_plot_hist, label=info['label'], c=info['c'], density=density, limits=limits) 
		data_points.append(y_points)

	ax_plot.set_xlabel(plotting_information['xlabel'], fontsize=20)
	uf.organise_ylabel(ax_plot, plotting_information['ylabel'], bins, units, limits, density=density)

	if log: ax_plot.set_yscale('log')

	uf.organise_ylims(ax_plot, data_points, plotting_information, log)


	uf.add_legend(ax_plot, legend_title)
	
	if extra_pyplot_commands != None: uf.employ_extra_pyplot_commands(ax_plot, extra_pyplot_commands)
	
	if figure_title is not None: uf.write_figure_title(figure_title, ax_plot)

	plt.sca(ax_plot)
	if not only_canvas: uf.savefig(filename, "plot_data")


def plot_pdf(pdf_list, filename='plot.pdf', axis='x', log=False, xlabel=None, ylabel=None, ymin=None, ymax=None,
	      		xmin=None, xmax=None, bins=50,
				extra_pyplot_commands=None, also_plot_hist=False, only_canvas=False, label=None, component_labels=None, 
				color='r', component_colors=None, density=False, units=None, legend_title=None,
				stack=False, plot_components=True, dash_signal=False,
				figure_title=None, alpha=None, component_alpha=None):

	mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=["#ffb366", "#6666ff", "#33cc33", "#ff6666", "#cc66ff", "#993333", "#ff6699", "#8c8c8c", "#999900", "#00cccc"]) 

	if not isinstance(pdf_list, list):
		pdf_list = [pdf_list]
	if not isinstance(color, list):
		color = [color]
	if not isinstance(alpha, list):
		alpha = [alpha]
	if not isinstance(label, list):
		label = [label]

	N_data = len(pdf_list)

	component_labels = uf.organise_component_options(component_labels)
	component_colors = uf.organise_component_options(component_colors)
	component_alpha = uf.organise_component_options(component_alpha)

	plotting_information = uf.get_empty_plotting_information(xlabel, ylabel, ymin, ymax, xmin, xmax)

	obs, limits = uf.get_range([pdf_list], plotting_information)

	for index in range(N_data):

		plotting_information[f'obj_{index}'] = {}
		
		plotting_information[f'obj_{index}']['pdf'] = pdf_list[index]

		try: plotting_information[f'obj_{index}']['label'] = label[index]
		except: plotting_information[f'obj_{index}']['label'] = None

		try: plotting_information[f'obj_{index}']['comp_labels'] = component_labels[f'obj_{index}']
		except: plotting_information[f'obj_{index}']['comp_labels'] = None

		try: plotting_information[f'obj_{index}']['c'] = color[index]
		except: plotting_information[f'obj_{index}']['c'] = color[0]

		try: plotting_information[f'obj_{index}']['comp_c'] = component_colors[f'obj_{index}']
		except: plotting_information[f'obj_{index}']['comp_c'] = None

		try: plotting_information[f'obj_{index}']['a'] = alpha[index]
		except: plotting_information[f'obj_{index}']['a'] = 1.

		try: plotting_information[f'obj_{index}']['comp_a'] = component_alpha[f'obj_{index}']
		except: plotting_information[f'obj_{index}']['comp_a'] = None


	if not only_canvas: fig = plt.figure(figsize=(13,10))
	ax_plot = axes.get_ax_1D()
	ax_plot.set_xlim(limits[0], limits[1])

	data_points = []
	for key in plotting_information.keys():
		if "obj_" not in key: continue
		info = plotting_information[key]

		normalisation = 1.
		if info['pdf'].is_extended:
			binW = (limits[1]-limits[0])/bins
			try:
				normalisation = info['pdf'].get_yield().read_value().numpy()*info['pdf'].numeric_integrate(obs).numpy()[0]*binW
			except:
				normalisation = info['pdf'].get_yield().read_value().numpy()*info['pdf'].numeric_integrate(obs).numpy()*binW


		x_values, y_values = pf.plot_1D_PDF(info['pdf'], normalisation=normalisation, ax=ax_plot, points=1000, axis='x', switch_axes=False, 
				     					stack=stack, total_pdf_color=info['c'], colors=info['comp_c'], plot_components=plot_components,
										linewidth=3, dash_signal=dash_signal, label=info['label'], labels=info['comp_labels'], limits=limits,
										alpha=info['a'], alphas=info['comp_a'])
		data_points.append(y_values)

	ax_plot.set_xlabel(plotting_information['xlabel'], fontsize=20)
	uf.organise_ylabel(ax_plot, plotting_information['ylabel'], bins, units, limits, density=density)

	if log: ax_plot.set_yscale('log')

	uf.organise_ylims(ax_plot, data_points, plotting_information, log)

	uf.add_legend(ax_plot, legend_title)
	
	if extra_pyplot_commands != None: uf.employ_extra_pyplot_commands(ax_plot, extra_pyplot_commands)

	if figure_title is not None: uf.write_figure_title(figure_title, ax_plot)

	plt.sca(ax_plot)
	if not only_canvas: uf.savefig(filename, "plot_pdf")


def plot_pdf_data(pdf_list, data, filename='plot.pdf', axis='x', log=False, xlabel=None, ylabel=None, ymin=None, ymax=None,
	      		xmin=None, xmax=None, bins=50,
				extra_pyplot_commands=None, also_plot_hist=False, only_canvas=False, data_label=None, label=None, component_labels=None, 
				color='r', data_color='k', component_colors=None, density=False, units=None, legend_title=None,
				stack=False, plot_components=True, dash_signal=False, weights=None, normalise_yields=False, pulls=True,
				figure_title=None, alpha=None, component_alpha=None, as_subplot=False):

	mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=["#ffb366", "#6666ff", "#33cc33", "#ff6666", "#cc66ff", "#993333", "#ff6699", "#8c8c8c", "#999900", "#00cccc"]) 

	if as_subplot:
		only_canvas = True
		pulls = False

	if not isinstance(pdf_list, list):
		pdf_list = [pdf_list]
	if isinstance(data, list):
		raise Exception("hadd that data mate, only provide a single data object...")
	if not isinstance(color, list):
		color = [color]
	if alpha is not None and not isinstance(alpha, list):
		alpha = [alpha]
	if not isinstance(label, list):
		label = [label]

	N_data = len(pdf_list)

	component_labels = uf.organise_component_options(component_labels)
	component_colors = uf.organise_component_options(component_colors)
	component_alpha = uf.organise_component_options(component_alpha)

	plotting_information = uf.get_empty_plotting_information(xlabel, ylabel, ymin, ymax, xmin, xmax)

	obs, limits = uf.get_range([pdf_list], plotting_information)

	for index in range(N_data):

		plotting_information[f'obj_{index}'] = {}
		
		plotting_information[f'obj_{index}']['pdf'] = pdf_list[index]

		try: plotting_information[f'obj_{index}']['label'] = label[index]
		except: plotting_information[f'obj_{index}']['label'] = None

		try: plotting_information[f'obj_{index}']['comp_labels'] = component_labels[f'obj_{index}']
		except: plotting_information[f'obj_{index}']['comp_labels'] = None

		try: plotting_information[f'obj_{index}']['c'] = color[index]
		except: plotting_information[f'obj_{index}']['c'] = color[0]

		try: plotting_information[f'obj_{index}']['comp_c'] = component_colors[f'obj_{index}']
		except: plotting_information[f'obj_{index}']['comp_c'] = None

		try: plotting_information[f'obj_{index}']['a'] = alpha[index]
		except: plotting_information[f'obj_{index}']['a'] = 1.

		try: plotting_information[f'obj_{index}']['comp_a'] = component_alpha[f'obj_{index}']
		except: plotting_information[f'obj_{index}']['comp_a'] = None

		if index == 0: plotting_information[f'obj_{index}']['rel_size'] = 1.
		else: plotting_information[f'obj_{index}']['rel_size'] = uf.get_rel_size(pdf_list[index], pdf_list[0], limits)
	
	if not only_canvas: fig = plt.figure(figsize=(13,10))

	if not as_subplot:
		if pulls:
			ax_plot, ax_pulls = axes.get_ax_1D_with_pulls()
		else:
			ax_plot = axes.get_ax_1D()
	else:
		ax_plot = plt.gca()

	ax_plot.set_xlim(limits[0], limits[1])

	if not isinstance(data, zfit.Data):
		data = uf.convert_to_zfitData(data, weights, limits)

	x_points, y_points, yerr_points, x_range_hist, normalisation_data = uf.plot_x_y_yerr(data, ax=ax_plot, bins=bins, axis=axis, 
														also_plot_hist=also_plot_hist, label=data_label, c=data_color, density=density, limits=limits) 
	
	data_points = [y_points]
	for key in plotting_information.keys():
		if "obj_" not in key: continue
		info = plotting_information[key]


		if info['pdf'].is_extended and not normalise_yields: # want to plot it with the correct yield
			weights = data.weights
			data_np = np.asarray(data.to_pandas(obs=obs))
			if weights is None: weights = np.ones(np.shape(data_np))
			else: weights = np.asarray(weights)
			sumW = np.sum(weights)
			try:
				normalisation = normalisation_data*(info['pdf'].get_yield().read_value().numpy()*info['pdf'].numeric_integrate(obs).numpy()[0]/sumW)
			except:
				normalisation = normalisation_data*(info['pdf'].get_yield().read_value().numpy()*info['pdf'].numeric_integrate(obs).numpy()/sumW)
		else:
			normalisation = normalisation_data

		if not info['pdf'].is_extended:
			normalisation *= info['rel_size']

		x_values, y_values = pf.plot_1D_PDF(info['pdf'], ax=ax_plot, normalisation=normalisation, points=1000, axis='x', switch_axes=False, 
				     					stack=stack, total_pdf_color=info['c'], colors=info['comp_c'], plot_components=plot_components,
										linewidth=3, dash_signal=dash_signal, label=info['label'], labels=info['comp_labels'], limits=limits,
										alpha=info['a'], alphas=info['comp_a'])
		data_points.append(y_values)

		if key == "obj_0":
			normalisation_pulls = normalisation

	ax_plot.set_xlabel(plotting_information['xlabel'], fontsize=20)
	uf.organise_ylabel(ax_plot, plotting_information['ylabel'], bins, units, limits, density=density)

	if log: ax_plot.set_yscale('log')

	uf.organise_ylims(ax_plot, data_points, plotting_information, log)

	uf.add_legend(ax_plot, legend_title)
	
	if extra_pyplot_commands != None: uf.employ_extra_pyplot_commands(ax_plot, extra_pyplot_commands)

	if pulls:
		pull_funcs.plot_pulls(pdf_list[0], x_points, y_points, yerr_points, x_range_hist, normalisation_pulls, bins, axis=axis, ax=ax_pulls)

	if figure_title is not None: uf.write_figure_title(figure_title, ax_plot)

	plt.sca(ax_plot)
	if not only_canvas: uf.savefig(filename, "plot_pdf_data")





















































