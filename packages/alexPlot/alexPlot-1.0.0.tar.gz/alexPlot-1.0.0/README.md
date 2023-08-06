# alexPlot

A simple plotting library for plotting [zfit](https://zfit.readthedocs.io/en/latest/) PDFs and datasets, this package contains functions useful for plotting in 1D. These plotting functions are built with matplotlib functions and make use of zfit.Space and zfit.pdf.SumPDF objects. By default asymmetric errors are applied and pulls are computed with PDF integrals. The libarary can be used with the `only_canvas` option to act like another normal matplotlib plotting function. 

```
                                                     ,ggggggggggg,                          
                            ,dPYb,                  dP"""88""""""Y8,,dPYb,             I8   
                            IP'`Yb                  Yb,  88      `8bIP'`Yb             I8   
                            I8  8I                   `"  88      ,8PI8  8I          88888888
                            I8  8'                       88aaaad8P" I8  8'             I8   
                  ,gggg,gg  I8 dP   ,ggg,      ,gg,   ,gg88"""""    I8 dP    ,ggggg,   I8   
                 dP"  "Y8I  I8dP   i8" "8i    d8""8b,dP" 88         I8dP    dP"  "Y8gggI8   
                i8'    ,8I  I8P    I8, ,8I   dP   ,88"   88         I8P    i8'    ,8I ,I8,  
               ,d8,   ,d8b,,d8b,_  `YbadP' ,dP  ,dP"Y8,  88        ,d8b,_ ,d8,   ,d8',d88b, 
               P"Y8888P"`Y88P'"Y88888P"Y8888"  dP"   "Y8 88        8P'"Y88P"Y8888P"  8P""Y8 
```

# Setting up

To install
```
git clone ssh://git@gitlab.cern.ch:7999/amarshal/alexPlot.git
pip install --no-dependencies -e .
python -c 'import alexPlot'
```

Then
```
import alexPlot

# to ask for help 
alexPlot.help()
# to ask for examples
alexPlot.examples()
# to overwrite default options
alexPlot.options.estimate_pulls = False
```

# Plotting data

```
import zfit
import numpy as np
import alexPlot

# plot using numpy array
data = np.random.normal(0,1,1000)
alexPlot.plot_data(data, figure_title='Numpy example')

# plot using a zfit dataset
obs = zfit.Space("x", limits=(-5, 5)) 
data = zfit.Data.from_numpy(obs=obs, array=data)
alexPlot.plot_data(data, also_plot_hist=True, color='tab:blue', figure_title='zfit example')
```

<img src="./examples/example_numpy.png" width=50% height=50%><img src="./examples/example_zfit.png" width=50% height=50%>

# Plotting pdf

```
# Example with KDE
obs = zfit.Space("x", limits=(-5, 5)) 
data = np.random.normal(0,1,1000)
data = zfit.Data.from_numpy(obs=obs, array=data)
model_KDE = zfit.pdf.GaussianKDE1DimV1(obs=obs, data=data, bandwidth='silverman')
alexPlot.plot_pdf(model_KDE)

# Example with an exponential plus a Gaussian
obs = zfit.Space("x", limits=(0, 30))
mean = zfit.Parameter("mean", 17,)
sigma = zfit.Parameter("sigma", 2,)
model_Gauss = zfit.pdf.Gauss(mean, sigma, obs)
lam = zfit.Parameter("lam", -0.1)
model_Exp = zfit.pdf.Exponential(lam, obs)
frac = zfit.Parameter("frac", 0.2,)
total_model = zfit.pdf.SumPDF([model_Gauss,model_Exp], obs=obs, fracs=[frac])
alexPlot.plot_pdf(total_model)
```

<img src="./examples/example_KDE.png" width=50% height=50%><img src="./examples/example_exp_plus_Gauss.png" width=50% height=50%>


# Plotting data and pdf

```
# Example with KDE
alexPlot.plot_pdf_data(model_KDE, data, filename='examples/example_KDE_data.png', figure_title='KDE')

# Example with an exponential plus a Gaussian
alexPlot.plot_pdf_data(total_model, data)
```
<img src="./examples/example_KDE_data.png" width=50% height=50%><img src="./examples/example_exp_plus_Gauss_data.png" width=50% height=50%>

# Extra functionality

```
# Add weights
alexPlot.plot_pdf_data(total_model, data_np, 
        weights=np.abs(np.random.normal(0,1,np.shape(data_np))), stack=True)

# Highlight a signal peak and zoom in
alexPlot.plot_pdf_data(total_model, data_np, dash_signal=True, ymax=50)
```
<img src="./examples/example_exp_plus_Gauss_data_weights.png" width=50% height=50%><img src="./examples/example_exp_plus_Gauss_data_dashed.png" width=50% height=50%>

```
# Add lables
alexPlot.plot_pdf_data(total_model, data, 
                       dash_signal=True, label='Total PDF',
                       component_labels=['Signal', 'Background'], 
                       xlabel=r'Some dimension (MeV/$c^2$)', units=r'MeV/$c^2$')

# Plot a log yscale
alexPlot.plot_pdf_data(total_model, data, log=True)
```
<img src="./examples/example_exp_plus_Gauss_data_dashed_labels.png" width=50% height=50%><img src="./examples/example_exp_plus_Gauss_data_dashed_labels_log.png" width=50% height=50%>


```
# Plot multiple datasets
data_A = np.random.normal(-1,1,1000)
data_B = np.random.normal(2,1,10000)
alexPlot.plot_data([data_A, data_B], color=['tab:blue','tab:red'], also_plot_hist=True, bins=35)

# Plot multiple datasets normalised
alexPlot.plot_data([data_A, data_B], label=['Dataset A', 'Dataset B'], 
                density=True, also_plot_hist=True, bins=35)
```
<img src="./examples/example_two.png" width=50% height=50%><img src="./examples/example_two_density.png" width=50% height=50%>

```
# Use custom pyplot commands
alexPlot.plot_pdf_data(total_model, data, log=True, 
                extra_pyplot_commands=["plt.axvline(x=15,c='k')"])

# Overlay custom pyplot objects
plt.figure(figsize=(13,10))
alexPlot.plot_pdf_data(total_model, data, only_canvas=True, stack=True, 
                component_colors=['tab:cyan','tab:grey'], color='r', pulls=False)
plt.axhline(y=10,c='r')
plt.savefig("examples/only_canvas.png")
plt.close("all")
```
<img src="./examples/example_exp_plus_Gauss_data_dashed_labels_log_pyplot.png" width=50% height=50%><img src="./examples/only_canvas.png" width=50% height=50%>

```
# Use xlims
alexPlot.plot_pdf_data(total_model, data, stack=True, xmin=10, xmax=22,
                component_colors=['tab:cyan','tab:grey'], color='r')

# Plot multiple PDFs at once (note stack only stacks PDFs within same SumPDF)
obs = zfit.Space("x", limits=(-5, 5)) 
data_np = np.random.normal(0,1,2500)
data = zfit.Data.from_numpy(obs=obs, array=data_np)
model_KDE_A = zfit.pdf.GaussianKDE1DimV1(obs=obs, data=data, bandwidth='silverman')
data = zfit.Data.from_numpy(obs=obs, array=data_np[:1250])
model_KDE_B = zfit.pdf.GaussianKDE1DimV1(obs=obs, data=data, bandwidth='silverman')
yield_A = zfit.Parameter("yield_A", 2500)
model_KDE_A.set_yield(yield_A)
yield_B = zfit.Parameter("yield_B", 1250)
model_KDE_B.set_yield(yield_B)
alexPlot.plot_pdf_data([model_KDE_A, model_KDE_B], data_np, color=["#ffb366",'b'], component_colors=[["#ffb366"],['b']], alpha=[1.,0.25], label=['plot_A', 'plot_B'], stack=True)

```
<img src="./examples/example_exp_plus_Gauss_data_dashed_labels_log_pyplot_lims.png" width=50% height=50%><img src="./examples/PDF_and_data_2_merge_data_yields_labels_stack.png" width=50% height=50%>


```
                                                     ,ggggggggggg,                          
                            ,dPYb,                  dP"""88""""""Y8,,dPYb,             I8   
                            IP'`Yb                  Yb,  88      `8bIP'`Yb             I8   
                            I8  8I                   `"  88      ,8PI8  8I          88888888
                            I8  8'                       88aaaad8P" I8  8'             I8   
                  ,gggg,gg  I8 dP   ,ggg,      ,gg,   ,gg88"""""    I8 dP    ,ggggg,   I8   
                 dP"  "Y8I  I8dP   i8" "8i    d8""8b,dP" 88         I8dP    dP"  "Y8gggI8   
                i8'    ,8I  I8P    I8, ,8I   dP   ,88"   88         I8P    i8'    ,8I ,I8,  
               ,d8,   ,d8b,,d8b,_  `YbadP' ,dP  ,dP"Y8,  88        ,d8b,_ ,d8,   ,d8',d88b, 
               P"Y8888P"`Y88P'"Y88888P"Y8888"  dP"   "Y8 88        8P'"Y88P"Y8888P"  8P""Y8 
```