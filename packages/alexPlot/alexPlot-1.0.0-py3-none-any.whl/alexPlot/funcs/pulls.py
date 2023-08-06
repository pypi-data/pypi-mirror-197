import alexPlot
import matplotlib.pyplot as plt
import numpy as np
import zfit

def plot_pulls(pdf, x_points, y_points, yerr_points, x_range_hist, normalisation, nbins, ax=None, axis='x', switch_axes=False, estimated_pulls=False):

	if ax == None:
		ax = plt.gca()

	axis = 'x'
	
	limits_array = np.asarray(pdf.space.limits)[:,0,:]
	limits_x = zfit.Space(pdf.obs[0], limits=(limits_array[0][0], limits_array[1][0]))

	if switch_axes or axis == 'y':
		limits_x, limits_y = limits_y, limits_x

	# Check whether PDF is a sum of component. How we iterate depends on this.
	if isinstance(pdf, zfit.pdf.SumPDF):
		pdf_iterator = zip(pdf.pdfs, pdf.params.values())
	else:
		pdf_iterator = zip([pdf], [1])
	
	if alexPlot.options.estimate_pulls:
		y_fit = np.zeros(nbins)
		for pdf_idx, (pdf_i, frac_i) in enumerate(pdf_iterator):		
			try:
				frac = pdf_i.get_yield().read_value().numpy()/pdf.get_yield().read_value().numpy()
			except:
				try:
					frac = frac_i.read_value().numpy()
				except:
					frac = frac_i

			y = pdf_i.pdf(x_points) * frac * normalisation
			y_fit += y

		if not isinstance(pdf, zfit.pdf.SumPDF):
			y_fit = pdf.pdf(x_points) * normalisation
	else:

		y_fit = np.zeros(nbins)
		for pdf_idx, (pdf_j, frac_j) in enumerate(pdf_iterator):
		
			# Do pulls properly
			y_fit_j = np.empty(0)
			for bin_idx in range(nbins):
				lower_i = x_range_hist[0] + ((x_range_hist[1]-x_range_hist[0])/nbins)*bin_idx
				upper_i = x_range_hist[0] + ((x_range_hist[1]-x_range_hist[0])/nbins)*(bin_idx+1)

				y_fit_j_i = pdf_j.numeric_integrate((lower_i,upper_i)) 
				
				binW = ((x_range_hist[1]-x_range_hist[0])/nbins)
				y_fit_j = np.append(y_fit_j, y_fit_j_i * normalisation * frac_j/binW)

			y_fit += y_fit_j





	if len(np.shape(yerr_points)) == 1:
		yerr_points_sided = yerr_points
	elif len(np.shape(yerr_points)) == 2:
		yerr_points_sided = yerr_points[0]
		yerr_points_sided[np.where((y_fit-y_points)>0)] = yerr_points[1][np.where((y_fit-y_points)>0)]
	pulls = (y_fit-y_points)/yerr_points_sided
	pulls = -1.*pulls

	colors = np.asarray(['#737373' for i in x_points])
	for pull_idx, pull in enumerate(pulls):
		if np.abs(pull) > 3.:
			colors[pull_idx] = '#f5a742'
		if np.abs(pull) > 5.:
			colors[pull_idx] = '#f54242'
	if switch_axes:
		ax.barh(x_points, pulls,color=colors,height=((x_range_hist[1]-x_range_hist[0])/nbins),align='center',alpha=1.)
		ax.axvline(x=0,c='k',linewidth=0.5)
		ax.set_xticks([-5,0,5],[-5,0,5])
		ax.set_xlim(-5, 5)
	else:
		ax.bar(x_points, pulls,color=colors,width=((x_range_hist[1]-x_range_hist[0])/nbins),align='center',alpha=1.)
		ax.axhline(y=0,c='k',linewidth=0.5)
		ax.set_yticks([-5,0,5],[-5,0,5])
		ax.set_ylim(-5, 5)