import alexPlot
import numpy as np
import zfit
from scipy.stats import poisson
from scipy.stats import norm
import pickle
import matplotlib.pyplot as plt

def convert_to_zfitData(data_list, weights_list, limits=None):
	if limits is None:
		if isinstance(data_list, list):
			np_array = np.empty(0)
			for item in data_list:
				np_array = np.concatenate((np_array, item))
		data_points = np.asarray(np_array).flatten()
		hist = np.histogram(data_points, bins=50)
		min_value, max_value = hist[1][0], hist[1][-1]
	else:
		min_value, max_value = limits[0], limits[1]
	
	if alexPlot.options.verbose: print("\n\nmin_value, max_value", min_value, max_value)
	obs = zfit.Space("x", limits=(min_value, max_value))

	if isinstance(data_list, list):
		zfit_data = []
		for index in range(len(data_list)):
			if weights_list is not None: 
				try: weights = np.asarray(weights_list[index])
				except: weights = np.asarray(weights)
			else: weights = weights_list
			zfit_data.append(zfit.Data.from_numpy(obs=obs, array=np.asarray(data_list[index]), weights=weights))
		return zfit_data
	else:
		if weights_list is not None: 
			weights = np.asarray(weights_list)
		else: weights = None
		return zfit.Data.from_numpy(obs=obs, array=np.asarray(data_list), weights=weights)

	

def plot_x_y_yerr(data, ax=None, axis='x', bins=50, label=None, also_plot_hist=False, c='k', density=False, limits=None):

	if ax == None:
		ax = plt.gca()

	if limits is None:
		limits_array = np.asarray(data.space.limits)[:,0,:]
		limits = [limits_array[0][0], limits_array[1][0]]
	
	obs = zfit.Space(data.obs[0], limits=(limits[0], limits[1]))

	data_np = np.asarray(data.to_pandas(obs=obs))

	weights = data.weights
	there_are_no_weights = False
	if weights is None: 
		weights = np.ones(np.shape(data_np))
		there_are_no_weights = True
	else: weights = np.expand_dims(np.asarray(weights),1)
	sumW = np.sum(weights)

	hist_i = np.histogram(data_np, bins=bins, range=limits, weights=weights)
	binw=hist_i[1][1]-hist_i[1][0]
	x_points = hist_i[1][:-1] + (hist_i[1][1]-hist_i[1][0])/2.
	y_points = hist_i[0]
	yerr_points = np.sqrt(np.histogram(data_np, bins=bins, range=[np.amin(hist_i[1]),np.amax(hist_i[1])], weights=weights*weights)[0])
	xerr_points = np.diff(hist_i[1])/2.
	np.histogram(data_np, bins=bins, range=[np.amin(hist_i[1]),np.amax(hist_i[1])])[0]

	if density:
		sum_y = np.sum(y_points)
		if there_are_no_weights:
			yerr_points = poisson_asym_errors(y_points)

		y_points = y_points/sum_y
		yerr_points = yerr_points/sum_y

		y_points = y_points/binw
		yerr_points = yerr_points/binw

	if there_are_no_weights and not density:
		yerr_points = poisson_asym_errors(y_points)

	p = ax.errorbar(x_points, y_points, yerr=yerr_points, xerr=xerr_points, color=c,marker='o',fmt=' ',capsize=2,linewidth=1.75, markersize=8,label=label,alpha=1.,zorder=100)

	if also_plot_hist:
		plt.hist(data_np, bins=bins, range=[np.amin(hist_i[1]),np.amax(hist_i[1])], weights=weights, histtype='step', 
	   				color=p[0].get_color(), density=density)

	normalisation = binw * sumW

	return x_points, y_points, yerr_points, [np.amin(hist_i[1]),np.amax(hist_i[1])], normalisation


def find_nearest(array, value):
	array = np.asarray(array)
	idx = (np.abs(array - value)).argmin()
	return idx

def poisson_asym_errors(y_points, avoid_errorbars_on_edges=True):
	# https://www.nikhef.nl/~ivov/Talks/2013_03_21_DESY_PoissonError.pdf option 4

	compute_up_to_N = 150
	try:
		import pkg_resources
		DATA_PATH = pkg_resources.resource_filename('alexPlot', 'number_storage/')
		poisson_asym_errors_lookup_table = pickle.load(open(f'{DATA_PATH}/poisson_asym_errors_lookup_table.pickle',"rb"))
	except:
		# make lookup table...
		print(f"Couldnt find {f'number_storage/poisson_asym_errors_lookup_table.pickle'}, making lookup table, this is slow but only needs to be computed once...")
		poisson_asym_errors_lookup_table = np.empty((compute_up_to_N+1,2))
		for y_point in range(compute_up_to_N+1):
			if y_point % 10 == 0: print(y_point,'/',compute_up_to_N)

			fracs = np.empty((0,3))
			for lambda_value_i_idx, lambda_value_i in enumerate(np.linspace(1E-9, 500, 5000)):

				t = np.linspace(0, 500, 501)
				d = poisson.pmf(t, lambda_value_i, loc=0)
				frac_below_i = np.sum(d[:int(y_point)+1])/np.sum(d)
				frac_above_i = np.sum(d[int(y_point):])/np.sum(d)
				fracs = np.append(fracs, [[lambda_value_i, frac_below_i, frac_above_i]], axis=0)

			error_low = fracs[:,0][find_nearest(fracs[:,2], norm.cdf(-1, loc=0, scale=1))]
			error_high = fracs[:,0][find_nearest(fracs[:,1], norm.cdf(-1, loc=0, scale=1))]

			error_low = y_point-error_low
			error_high = error_high-y_point

			poisson_asym_errors_lookup_table[y_point][0] = error_low
			poisson_asym_errors_lookup_table[y_point][1] = error_high

		with open(f'number_storage/poisson_asym_errors_lookup_table.pickle', 'wb') as handle:
			pickle.dump(poisson_asym_errors_lookup_table, handle, protocol=pickle.HIGHEST_PROTOCOL)
		print(f"Saved {f'number_storage/poisson_asym_errors_lookup_table.pickle'} for next time.")

	try:
		first_bin = np.amin(np.where(y_points>0))-1
		last_bin = np.amax(np.where(y_points>0))+1
	except:
		first_bin = 0
		last_bin = 0
		avoid_errorbars_on_edges = False

	y_errors_asym = np.zeros((2,np.shape(y_points)[0]))

	for y_point_idx, y_point in enumerate(y_points):
		if (y_point_idx < first_bin or y_point_idx > last_bin) and avoid_errorbars_on_edges:
			error_low = 0.
			error_high = 0.
		elif y_point > compute_up_to_N:
			y_err = np.sqrt(y_point)
			error_low = y_err
			error_high = y_err
		else:
			if alexPlot.options.no_errors_on_zero_bins and int(y_point)==0:
				error_low = 0
				error_high = 0
			else:
				error_low = poisson_asym_errors_lookup_table[int(y_point)][0]
				error_high = poisson_asym_errors_lookup_table[int(y_point)][1]

		y_errors_asym[0][y_point_idx] = error_low
		y_errors_asym[1][y_point_idx] = error_high

	return y_errors_asym
    
def organise_axes(ax_plot, xlabel, values, ymin, ymax, log):
	ax_plot.set_xlabel(xlabel, fontsize=20)
	
	if log:
		ax_plot.set_ylim(ymin=0.25*np.amin(np.asarray(values)[np.where(np.asarray(values)>0)]))
	if ymin != None:
		ax_plot.set_ylim(ymin=ymin)
	else:
		if np.shape(np.where(values<0))[1] == 0 and not log:
			ax_plot.set_ylim(ymin=0)

	if ymax != None:
		ax_plot.set_ylim(ymax=ymax)
	
	if log:
		plt.yscale('log')

def employ_extra_pyplot_commands(ax_plot, extra_pyplot_commands):
	plt.sca(ax_plot)
	try:
		for item in extra_pyplot_commands: 
			eval(item)
	except:
		eval(extra_pyplot_commands)

def write_figure_title(figure_title, ax_plot):
	plt.text(0.04, 0.96, figure_title, fontsize=40, horizontalalignment='left',verticalalignment='top', transform=ax_plot.transAxes)

def add_legend(ax_plot, legend_title):
	h, l = ax_plot.get_legend_handles_labels()
	if len(h) != 0:
		legend = ax_plot.legend()
		if legend_title is not None:
			legend.set_title(legend_title)

def savefig(filename, func):
	if alexPlot.options.bbox_inches == 'tight':
		plt.savefig(filename, bbox_inches='tight')
	else:
		plt.savefig(filename)
	print(f"Plotting ({func}) and saving figure in:",filename)
	plt.close('all')
	

def organise_component_options(component):
	component_dict = {}
	component_index = 0
	if component is not None:
		for component_i in component:
			if not isinstance(component_i, list):
				component_dict[f'obj_{component_index}'] = component
				break
			else:
				try:
					component_dict[f'obj_{component_index}'] = component_i
					component_index += 1
				except: pass
		return component_dict
	else:
		return None


def get_rel_size(pdf_i, pdf_0, limits):

	if pdf_i.is_extended:
		relative_pdf_size = (pdf_i.get_yield().read_value().numpy()/pdf_0.get_yield().read_value().numpy())
		relative_pdf_size *= np.sum(pdf_i.unnormalized_pdf(np.linspace(limits[0], limits[1],500)))/np.sum(pdf_0.unnormalized_pdf(np.linspace(limits[0], limits[1],500)))
	else:
		relative_pdf_size = np.sum(pdf_i.unnormalized_pdf(np.linspace(limits[0], limits[1],500)))/np.sum(pdf_0.unnormalized_pdf(np.linspace(limits[0], limits[1],500)))

	return relative_pdf_size

def get_empty_plotting_information(xlabel, ylabel, ymin, ymax, xmin, xmax):

	plotting_information = {}

	plotting_information['xlabel'] = xlabel
	plotting_information['ylabel'] = ylabel

	plotting_information['ymin'] = ymin
	plotting_information['ymax'] = ymax

	plotting_information['xmin'] = xmin
	plotting_information['xmax'] = xmax

	return plotting_information

def flatten(l):
    return [item for sublist in l for item in sublist]

def get_range(items, plotting_information):

	items = flatten(items)
	obs_list = []
	range_list = np.empty((len(items),2))
	for item_idx, item in enumerate(items):

		limits_array = np.asarray(item.space.limits)[:,0,:]

		range_list[item_idx][0] = limits_array[0][0]
		range_list[item_idx][1] = limits_array[1][0]

		obs_list.append(item.obs[0])

	if np.shape(np.unique(np.asarray(obs_list)))[0] != 1:
		raise Exception("All items must have the same observable...")

	if np.shape(np.unique(range_list[:,0]))[0] != 1 or np.shape(np.unique(range_list[:,1]))[0] != 1:
		raise Exception("The limits of all items must be equal...")

	limits = [np.amin(range_list[:,0]), np.amax(range_list[:,1])]

	if plotting_information["xmin"] != None: limits[0] = plotting_information["xmin"]
	if plotting_information["xmax"] != None: limits[1] = plotting_information["xmax"]

	obs = zfit.Space(np.unique(np.asarray(obs_list))[0], limits=(limits[0], limits[1]))

	return obs, limits

def organise_ylabel(ax, ylabel, bins, units, limits, density=False):
	if ylabel == None:
		if units == None: units = ''
		else: units = ' '+units
		if density:
			ax.set_ylabel(f'Event density', fontsize=25)
		else:
			ax.set_ylabel(f'Events / ({((limits[1]-limits[0])/bins):.2f}{units})', fontsize=25)
	else:
		ax.set_ylabel(ylabel, fontsize=20)

def organise_ylims(ax, data_points, info, log):
	if isinstance(data_points, list):
		np_array = np.empty(0)
		for item in data_points:
			np_array = np.concatenate((np_array, item))
		data_points = np_array
	data_points = np.asarray(data_points).flatten()
	if info['ymin'] != None:
		ax.set_ylim(ymin=info['ymin'])
	else:
		if np.shape(np.where(data_points<0))[1] == 0 and not log:
			ax.set_ylim(ymin=0)
		if log:
			ax.set_ylim(ymin=0.1*np.amin(data_points[np.where(data_points>0)]))

	if info['ymax'] != None:
		ax.set_ylim(ymax=info['ymax'])