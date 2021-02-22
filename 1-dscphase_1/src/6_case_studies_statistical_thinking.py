  #--  --  --  -- Case Studies in Statistical Thinking:
# Used for Data Scientist Training Path 
#FYI it's a compilation of how to work
#with different commands.


### --------------------------------------------------------
# # ------>>>>> EDA: Plot ECDFs of active bout length
# Import the dc_stat_think module as dcst
import dc_stat_think as dcst
# Generate x and y values for plotting ECDFs
x_wt, y_wt = dcst.ecdf(bout_lengths_wt)
x_mut, y_mut = dcst.ecdf(bout_lengths_mut)
# Plot the ECDFs
_ = plt.plot(x_wt, y_wt, marker='.', linestyle='none')
_ = plt.plot(x_mut, y_mut, marker='.', linestyle='none')
# Make a legend, label axes, and show plot
_ = plt.legend(('wt', 'mut'))
_ = plt.xlabel('active bout length (min)')
_ = plt.ylabel('ECDF')
plt.show()


### --------------------------------------------------------
# # ------>>>>> Interpreting ECDFs and the story
# R/ The bout lengths appear Exponentially distributed, 
# which implies that exiting an active bout to rest is a 
# Poisson process; the fish have no apparent memory 
# about when they became active.


### --------------------------------------------------------
# # ------>>>>> Parameter estimation: active bout length
# Compute mean active bout length
mean_wt = np.mean(bout_lengths_wt)
mean_mut = np.mean(bout_lengths_mut)
 
# Draw bootstrap replicates
bs_reps_wt = dcst.draw_bs_reps(bout_lengths_wt, np.mean, size=10000)
bs_reps_mut = dcst.draw_bs_reps(bout_lengths_mut, np.mean, size=10000)
 
# Compute 95% confidence intervals
conf_int_wt = np.percentile(bs_reps_wt, [2.5, 97.5])
conf_int_mut = np.percentile(bs_reps_mut, [2.5, 97.5])
 
# Print the results
print("""
wt:  mean = {0:.3f} min., conf. int. = [{1:.1f}, {2:.1f}] min.
mut: mean = {3:.3f} min., conf. int. = [{4:.1f}, {5:.1f}] min.
""".format(mean_wt, *conf_int_wt, mean_mut, *conf_int_mut))
 
# wt:  mean = 3.874 min., conf. int. = [3.6, 4.1] min.
# mut: mean = 6.543 min., conf. int. = [6.1, 7.0] min.



### --------------------------------------------------------
# # ------>>>>> Permutation test: wild type versus heterozygote
# Compute the difference of means: diff_means_exp
diff_means_exp = np.mean(bout_lengths_het) - np.mean(bout_lengths_wt)
# Draw permutation replicates: perm_reps
perm_reps = dcst.draw_perm_reps(bout_lengths_het, bout_lengths_wt, dcst.diff_of_means, size=10000)
# Compute the p-value: p-val
p_val = np.sum(perm_reps >= diff_means_exp) / len(perm_reps)
# Print the result
print('p =', p_val)



### --------------------------------------------------------
# # ------>>>>> Bootstrap hypothesis test
# Concatenate arrays: bout_lengths_concat
bout_lengths_concat = np.concatenate((bout_lengths_wt, bout_lengths_het))
 
# Compute mean of all bout_lengths: mean_bout_length
mean_bout_length = np.mean(bout_lengths_concat)
 
# Generate shifted arrays
wt_shifted = bout_lengths_wt - np.mean(bout_lengths_wt) + mean_bout_length
het_shifted = bout_lengths_het - np.mean(bout_lengths_het) + mean_bout_length
 
# Compute 10,000 bootstrap replicates from shifted arrays
bs_reps_wt = dcst.draw_bs_reps(wt_shifted, np.mean, size=10000)
bs_reps_het = dcst.draw_bs_reps(het_shifted, np.mean, size=10000)
# Get replicates of difference of means: bs_replicates
bs_reps = bs_reps_het - bs_reps_wt
# Compute and print p-value: p
p = np.sum(bs_reps >= diff_means_exp) / len(bs_reps)
print('p-value =', p)




### --------------------------------------------------------
# # ------>>>>> Assessing the growth rate
# Compute logarithm of the bacterial area: log_bac_area
log_bac_area = np.log(bac_area)
# Compute the slope and intercept: growth_rate, log_a0
growth_rate, log_a0 = np.polyfit(t, log_bac_area, 1)
# Draw 10,000 pairs bootstrap replicates: growth_rate_bs_reps, log_a0_bs_reps
growth_rate_bs_reps, log_a0_bs_reps = dcst.draw_bs_pairs_linreg(t, log_bac_area, size=10000)   
# Compute confidence intervals: growth_rate_conf_int
growth_rate_conf_int = np.percentile(growth_rate_bs_reps, [2.5, 97.5])
# Print the result to the screen
print("""
Growth rate: {0:.4f} 1/hour
95% conf int: [{1:.4f}, {2:.4f}] 1/hour
""".format(growth_rate, *growth_rate_conf_int))


### --------------------------------------------------------
# # ------>>>>> Plotting the growth curve
# Plot data points in a semilog-y plot with axis labeles
_ = plt.semilogy(t, bac_area, marker='.', linestyle='none')
# Generate x-values for the bootstrap lines: t_bs
t_bs = np.array([0, 14])
# Plot the first 100 bootstrap lines
for i in range(100):
    y = np.exp(growth_rate_bs_reps[i] * t_bs + log_a0_bs_reps[i])
    _ = plt.semilogy(t_bs, y, linewidth=0.5, alpha=0.05, color='red')
# Label axes and show plot
_ = plt.xlabel('time (hr)')
_ = plt.ylabel('area (sq. µm)')
plt.show()


### --------------------------------------------------------
# # ------>>>>> Graphical EDA of men's 200 free heats
# Generate x and y values for ECDF: x, y
x, y = dcst.ecdf(mens_200_free_heats)
# Plot the ECDF as dots
plt.plot(x, y, marker='.', linestyle='none')
# Label axes and show plot
plt.xlabel('time (s)')
plt.ylabel('ECDF')
plt.show()



### --------------------------------------------------------
# # ------>>>>> 200 m free time with confidence interval
# Compute mean and median swim times
mean_time = np.mean(mens_200_free_heats)
median_time = np.median(mens_200_free_heats)
# Draw 10,000 bootstrap replicates of the mean and median
bs_reps_mean = dcst.draw_bs_reps(mens_200_free_heats, np.mean, size=10000)
bs_reps_median = dcst.draw_bs_reps(mens_200_free_heats, np.median, size=10000)
# Compute the 95% confidence intervals
conf_int_mean = np.percentile(bs_reps_mean, [2.5, 97.5])
conf_int_median = np.percentile(bs_reps_median, [2.5, 97.5])
# Print the result to the screen
print("""
mean time: {0:.2f} sec.
95% conf int of mean: [{1:.2f}, {2:.2f}] sec.

median time: {3:.2f} sec.
95% conf int of median: [{4:.2f}, {5:.2f}] sec.
""".format(mean_time, *conf_int_mean, median_time, *conf_int_median))

### --------------------------------------------------------
# # ------>>>>> EDA: finals versus semifinals
# Compute fractional difference in time between finals and semis
f = (semi_times - final_times) / semi_times
# Generate x and y values for the ECDF: x, y
x, y = dcst.ecdf(f)
# Make a plot of the ECDF
plt.plot(x, y, marker='.', linestyle='none')
# Label axes and show plot
_ = plt.xlabel('f')
_ = plt.ylabel('ECDF')
plt.show()


### --------------------------------------------------------
# # ------>>>>> Parameter estimates of difference between finals and semifinals
# Mean fractional time difference: f_mean
f_mean = np.mean(f)
# Get bootstrap reps of mean: bs_reps
bs_reps = dcst.draw_bs_reps(f, func=np.mean, size=10000)
# Compute confidence intervals: conf_int
conf_int = np.percentile(bs_reps, [2.5, 97.5])
# Report
print("""
mean frac. diff.: {0:.5f}
95% conf int of mean frac. diff.: [{1:.5f}, {2:.5f}]""".format(f_mean, *conf_int))


### --------------------------------------------------------
# # ------>>>>> How to do the permutation test
# Based on our EDA and 
# parameter estimates, it is 
# tough to discern improvement 
# from the semifinals to 
# finals. In the next exercise, 
# you will test the hypothesis 
# that there is no difference 
# in performance between the 
# semifinals and finals. A 
# permutation test is fitting 
# for this. We will use the 
# mean value of f as the test 
# statistic. Which of the 
# following simulates getting 
# the test statistic under the 
# null hypothesis? 

# Strategy 1 Take an array of 
# semifinal times and an array 
# of final times for each 
# swimmer for each 
# stroke/distance pair. Go 
# through each array, and for 
# each index, swap the entry in 
# the respective final and 
# semifinal array with a 50% 
# probability. Use the 
# resulting final and semifinal 
# arrays to compute f and then 
# the mean of f. Strategy 2 
# Take an array of semifinal 
# times and an array of final 
# times for each swimmer for 
# each stroke/distance pair and 
# concatenate them, giving a 
# total of 96 entries. Scramble 
# the concatenated array using 
# the np.permutation() 
# function. Assign the first 48 
# entries in the scrambled 
# array to be "semifinal" and 
# the last 48 entries to be 
# "final." Compute f from these 
# new semifinal and final 
# arrays, and then compute the 
# mean of f. Strategy 3 Take 
# the array f we used in the 
# last exercise. Multiply each 
# entry of f by either 1 or -1 
# with equal probability. 
# Compute the mean of this new 
# array to get the test 
# statistic. Strategy 4 Define 
# a function with signature 
# compute_f(semi_times, 
# final_times) to compute f 
# from inputted swim time 
# arrays. Draw a permutation 
# replicate using 
# dcst.draw_perm_reps(
# semi_times, final_times, 
# compute_f)
# R/ Strategy 1


### --------------------------------------------------------
# # ------>>>>> Generating permutation samples
def swap_random(a, b):
    """Randomly swap entries in two arrays."""
    # Indices to swap
    swap_inds = np.random.random(size=len(a)) < 0.5 
    # Make copies of arrays a and b for output
    a_out = np.copy(a)
    b_out = np.copy(b)
    # Swap values
    a_out[swap_inds] = b[swap_inds]
    b_out[swap_inds] = a[swap_inds]
 
    return a_out, b_out


### --------------------------------------------------------
# # ------>>>>> Hypothesis test: Do women swim the same way in semis and finals?
# Set up array of permutation replicates
perm_reps = np.empty(1000)
for i in range(1000):
    # Generate a permutation sample
    semi_perm, final_perm = swap_random(semi_times, final_times)    
    # Compute f from the permutation sample
    f = (semi_perm - final_perm) / semi_perm  
    # Compute and store permutation replicate
    perm_reps[i] = np.mean(f)
# Compute and print p-value
print('p =', np.sum(perm_reps >= f_mean) / 1000)


### --------------------------------------------------------
# # ------>>>>> EDA: Plot all your data
# Plot the splits for each swimmer
for splitset in splits:
    _ = plt.plot(split_number, splitset, linewidth=1, color='lightgray')
# Compute the mean split times
mean_splits = np.mean(splits, axis=0)
# Plot the mean split times
_ = plt.plot(split_number, mean_splits, linewidth=3, markersize=12)
# Label axes and show plot
_ = plt.xlabel('split number')
_ = plt.ylabel('split time (s)')
plt.show()


### --------------------------------------------------------
# # ------>>>>> Linear regression of average split time
# Perform regression
slowdown, split_3 = np.polyfit(split_number, mean_splits, deg=1)
 
# Compute pairs bootstrap
bs_reps, _ = dcst.draw_bs_pairs_linreg(split_number, mean_splits, size=10000)
# Compute confidence interval
conf_int = np.percentile(bs_reps, [2.5, 97.5])
# Plot the data with regressions line
_ = plt.plot(split_number, mean_splits, marker='.', linestyle='none')
_ = plt.plot(split_number, slowdown * split_number + split_3, '-')
# Label axes and show plot
_ = plt.xlabel('split number')
_ = plt.ylabel('split time (s)')
plt.show()
# Print the slowdown per split
print("""
mean slowdown: {0:.3f} sec./split
95% conf int of mean slowdown: [{1:.3f}, {2:.3f}] sec./split""".format(
    slowdown, *conf_int))


### --------------------------------------------------------
# # ------>>>>>Hypothesis test: are they slowing down?
# A metric for improvement In 
# your first analysis, you will 
# investigate how times of 
# swimmers in 50 m events 
# change as they move between 
# low numbered lanes (1-3) to 
# high numbered lanes (6-8) in 
# the semifinals and finals. We 
# showed in the previous 
# chapter that there is little 
# difference between semifinal 
# and final performance, so you 
# will neglect any differences 
# due to it being the final 
# versus the semifinal. 

# You want to use as much data 
# as you can, so use all four 
# strokes for both the men's 
# and women's competitions. As 
# such, what would be a good 
# metric for improvement from 
# one round to the next for an 
# individual swimmer, where ta 
# is the swim time in a low 
# numbered lane and tb is the 
# swim time in a high numbered 
# lane?
# R/The fractional improvement of swim time, (ta - tb) / ta.


### --------------------------------------------------------
# # ------>>>>> ECDF of improvement from low to high lanes
# Compute the fractional improvement of being in high lane: f
f = (swimtime_low_lanes - swimtime_high_lanes) / swimtime_low_lanes
# Make x and y values for ECDF: x, y
x, y = dcst.ecdf(f)
 
# Plot the ECDFs as dots
_ = plt.plot(x, y, marker='.', linestyle='none')
# Label the axes and show the plot
_ = plt.xlabel('f')
_ = plt.ylabel('ECDF')
plt.show()



### --------------------------------------------------------
# # ------>>>>> Estimation of mean improvement
# Compute the mean difference: f_mean
f_mean = np.mean(f) 
# Draw 10,000 bootstrap replicates: bs_reps
bs_reps = dcst.draw_bs_reps(f, np.mean, size=10000)
# Compute 95% confidence interval: conf_int
conf_int = np.percentile(bs_reps, [2.5, 97.5])
# Print the result
print("""
mean frac. diff.: {0:.5f}
95% conf int of mean frac. diff.: [{1:.5f}, {2:.5f}]""".format(f_mean, *conf_int))


### --------------------------------------------------------
# # ------>>>>> How should we test the hypothesis?
# You are interested in the 
# presence of lane bias toward 
# higher lanes, presumably due 
# to a slight current in the 
# pool. A natural null 
# hypothesis to test, then, is 
# that the mean fractional 
# improvement going from low to 
# high lane numbers is zero. 
# Which of the following is a 
# good way to simulate this 
# null hypothesis? 

# As a reminder, the arrays 
# swimtime_low_lanes and 
# swimtime_high_lanes contain 
# the swim times for lanes 1-3 
# and 6-8, respectively, and we 
# define the fractional 
# improvement as f = (
# swimtime_low_lanes - 
# swimtime_high_lanes) / 
# swimtime_low_lanes.
# R/ Subtract the mean of f from f to generate f_shift. Then, take bootstrap replicate of the mean from this f_shift.


### --------------------------------------------------------
# # ------>>>>> Hypothesis test: Does lane assignment affect performance?
# Shift f: f_shift
f_shift = f - f_mean
# Draw 100,000 bootstrap replicates of the mean: bs_reps
bs_reps = dcst.draw_bs_reps(f_shift, np.mean, size=100000)
# Compute and report the p-value
p_val = np.sum(bs_reps >= f_mean) / 100000
print('p =', p_val)


### --------------------------------------------------------
# # ------>>>>> Did the 2015 event have this problem?
# Compute f and its mean
f = (swimtime_low_lanes_15 - swimtime_high_lanes_15) / swimtime_low_lanes_15
f_mean = np.mean(f)
# Draw 10,000 bootstrap replicates
bs_reps = dcst.draw_bs_reps(f, np.mean, size=10000)
# Compute 95% confidence interval
conf_int = np.percentile(bs_reps, [2.5, 97.5])
# Shift f
f_shift = f - f_mean
# Draw 100,000 bootstrap replicates of the mean
bs_reps = dcst.draw_bs_reps(f_shift, np.mean, size=100000)
# Compute the p-value
p_val = np.sum(bs_reps >= f_mean) / 100000
# Print the results
print("""
mean frac. diff.: {0:.5f}
95% conf int of mean frac. diff.: [{1:.5f}, {2:.5f}]
p-value: {3:.5f}""".format(f_mean, *conf_int, p_val))


### --------------------------------------------------------
# # ------>>>>>Which splits should we 
# consider? As you proceed to 
# quantitatively analyze the 
# zigzag effect in the 1500 m, 
# which splits should you 
# include in our analysis? For 
# reference, the plot of the 
# zigzag effect from the video 
# is shown to the right.
# R/You should include all splits except the first two and the 
# last two. You should neglect the last two because swimmers 
# stop pacing themselves and "kick" for the final stretch. The 
# first two are different because they involve jumping off the 
# starting blocks and more underwater swimming than others.


### --------------------------------------------------------
# # ------>>>>> EDA: mean differences between odd and even splits
# Plot the the fractional difference for 2013 and 2015
plt.plot(lanes, f_13, marker='.', markersize=12, linestyle='none')
plt.plot(lanes, f_15, marker='.', markersize=12, linestyle='none')
# Add a legend
_ = plt.legend((2013, 2015))
# Label axes and show plot
plt.xlabel('lane')
plt.ylabel('frac. diff. (odd - even)')
plt.show()


### --------------------------------------------------------
# # ------>>>>> How does the current effect depend on lane position?
# Compute the slope and intercept of the frac diff/lane curve
slope, intercept  = np.polyfit(lanes, f_13, 1)
# Compute bootstrap replicates
bs_reps_slope, bs_reps_int = dcst.draw_bs_pairs_linreg(lanes, f_13, size=10000)
# Compute 95% confidence interval of slope
conf_int = np.percentile(bs_reps_slope, [2.5, 97.5])
# Print slope and confidence interval
print("""
slope: {0:.5f} per lane
95% conf int: [{1:.5f}, {2:.5f}] per lane""".format(slope, *conf_int))
# x-values for plotting regression lines
x = np.array([1, 8])
# Plot 100 bootstrap replicate lines
for i in range(100):
    _ = plt.plot(x, bs_reps_slope[i] * x + bs_reps_int[i], 
                 color='red', alpha=0.2, linewidth=0.5)
# Update the plot
plt.draw()
plt.show()


### --------------------------------------------------------
# # ------>>>>> Hypothesis test: can this be by chance?
# Compute observed correlation: rho
rho = dcst.pearson_r(lanes, f_13)
# Initialize permutation reps: perm_reps_rho
perm_reps_rho = np.empty(10000)
# Make permutation reps
for i in range(10000):
    # Scramble the lanes array: scrambled_lanes
    scrambled_lanes = np.random.permutation(lanes)
     
    # Compute the Pearson correlation coefficient
    perm_reps_rho[i] = dcst.pearson_r(scrambled_lanes, f_13)   
# Compute and print p-value
p_val = np.sum(perm_reps_rho >= rho) / 10000
print('p =', p_val)


### --------------------------------------------------------
# # ------>>>>>Parkfield earthquake magnitudes
# Make the plot
plt.plot(*dcst.ecdf(mags), marker='.', linestyle='none')
# Label axes and show plot
plt.xlabel('magnitude')
plt.ylabel('ECDF')
plt.show()


### --------------------------------------------------------
# # ------>>>>> Computing the b-value
def b_value(mags, mt, perc=[2.5, 97.5], n_reps=None):
    """Compute the b-value and optionally its confidence interval."""
    # Extract magnitudes above completeness threshold: m
    m = mags[mags >= mt]
    # Compute b-value: b
    b = (np.mean(m) - mt) * np.log(10)
 
    # Draw bootstrap replicates
    if n_reps is None:
        return b
    else:
        m_bs_reps = dcst.draw_bs_reps(m, np.mean, size=n_reps)
        # Compute b-value from replicates: b_bs_reps
        b_bs_reps = (m_bs_reps - mt) * np.log(10)
        # Compute confidence interval: conf_int
        conf_int = np.percentile(b_bs_reps, perc) 
        return b, conf_int


### --------------------------------------------------------
# # ------>>>>> The b-value for Parkfield
# Compute b-value and confidence interval
b, conf_int = b_value(mags, mt, perc=[2.5, 97.5], n_reps=10000)
# Generate samples to for theoretical ECDF
m_theor = np.random.exponential(b/np.log(10), size=100000) + mt
# Plot the theoretical CDF
_ = plt.plot(*dcst.ecdf(m_theor)) 
# Plot the ECDF (slicing mags >= mt)
_ = plt.plot(*dcst.ecdf(mags[mags >= mt]), marker='.', linestyle='none')
# Pretty up and show the plot
_ = plt.xlabel('magnitude')
_ = plt.ylabel('ECDF')
_ = plt.xlim(2.8, 6.2)
plt.show()
# Report the results
print("""
b-value: {0:.2f}
95% conf int: [{1:.2f}, {2:.2f}]""".format(b, *conf_int))


### --------------------------------------------------------
# # ------>>>>> Interearthquake time estimates for Parkfield
# Compute the mean time gap: mean_time_gap
mean_time_gap = np.mean(time_gap)
 
# Standard deviation of the time gap: std_time_gap
std_time_gap = np.std(time_gap)
 
# Generate theoretical Exponential distribution of timings: time_gap_exp
time_gap_exp = np.random.exponential(scale=mean_time_gap, size=10000)
 
# Generate theoretical Normal distribution of timings: time_gap_norm
time_gap_norm = np.random.normal(loc=mean_time_gap, scale=std_time_gap, size=10000)
 
# Plot theoretical CDFs
_ = plt.plot(*dcst.ecdf(time_gap_exp))
_ = plt.plot(*dcst.ecdf(time_gap_norm))
 
# Plot Parkfield ECDF
_ = plt.plot(*dcst.ecdf(time_gap, formal=True, min_x=-10, max_x=50))
 
# Add legend
_ = plt.legend(('Exp.', 'Norm.'), loc='upper left')
# Label axes, set limits and show plot
_ = plt.xlabel('time gap (years)')
_ = plt.ylabel('ECDF')
_ = plt.xlim(-10, 50)
plt.show()


### --------------------------------------------------------
# # ------>>>>> When will the next big Parkfield quake be?
# Draw samples from the Exponential distribution: exp_samples
exp_samples = np.random.exponential(scale=mean_time_gap, size=100000)
 
# Draw samples from the Normal distribution: norm_samples
norm_samples = np.random.normal(loc=mean_time_gap, scale=std_time_gap, size=100000)
 
# No earthquake as of today, so only keep samples that are long enough
exp_samples = exp_samples[exp_samples > today - last_quake]
norm_samples = norm_samples[norm_samples > today - last_quake]
 
# Compute the confidence intervals with medians
conf_int_exp = np.percentile(exp_samples, [2.5, 50, 97.5]) + last_quake
conf_int_norm = np.percentile(norm_samples, [2.5, 50, 97.5]) + last_quake
 
# Print the results
print('Exponential:', conf_int_exp)
print('     Normal:', conf_int_norm)


### --------------------------------------------------------
# # ------>>>>> Computing the value of a formal ECDF
# To be able to do the 
# Kolmogorov-Smirnov test, we 
# need to compute the value of 
# a formal ECDF at arbitrary 
# points. In other words, we 
# need a function, ecdf_formal(
# x, data) that returns the 
# value of the formal ECDF 
# derived from the data set 
# data for each value in the 
# array x. Two of the functions 
# accomplish this. One will 
# not. Of the two that do the 
# calculation correctly, one is 
# faster. Label each. 

# As a reminder, the ECDF is 
# formally defined as ECDF(x) 
# = (number of samples ≤ x) / (
# total number of samples). You 
# also might want to check out 
# the doc string of 
# np.searchsorted(). 

# a) 

# def ecdf_formal(x, data): 
# return np.searchsorted(
# np.sort(data), x) / len(data) 
# b) 

# def ecdf_formal(x, data): 
# return np.searchsorted(
# np.sort(data), x, 
# side='right') / len(data) c) 

# def ecdf_formal(x, data): 
# output = np.empty(len(x)) 

# data = np.sort(data) 

# for i, x_val in x: j = 0 
# while j < len(data) and 
# x_val >= data[j]: j += 1 

# output[i] = j 

# return output / len(data)
#R/ ----> (a) Incorrect; (b) Correct, fast; (c) Correct, slow.


### --------------------------------------------------------
# # ------>>>>> Computing the K-S statistic
def ks_stat(data1, data2):
    # Compute ECDF from data: x, y
    x, y = dcst.ecdf(data1)
     
    # Compute corresponding values of the target CDF
    cdf = dcst.ecdf_formal(x, data2)
 
    # Compute distances between concave corners and CDF
    D_top = y - cdf
    # Compute distance between convex corners and CDF
    D_bottom = cdf - y + 1/len(data1)
    return np.max((D_top, D_bottom))


### --------------------------------------------------------
# # ------>>>>> Drawing K-S replicates
def draw_ks_reps(n, f, args=(), size=10000, n_reps=10000):
    # Generate samples from target distribution
    x_f = f(*args, size=size)
     
    # Initialize K-S replicates
    reps = np.empty(n_reps)
     
    # Draw replicates
    for i in range(n_reps):
        # Draw samples for comparison
        x_samp = f(*args, size=n)
         
        # Compute K-S statistic
        reps[i] = dcst.ks_stat(x_samp, x_f)
 
    return reps


### --------------------------------------------------------
# # ------>>>>> The K-S test for Exponentiality
# Draw target distribution: x_f
x_f = np.random.exponential(scale=mean_time_gap, size=10000)
# Compute K-S stat: d
d = dcst.ks_stat(x_f, time_gap)
# Draw K-S replicates: reps
reps = dcst.draw_ks_reps(len(time_gap), np.random.exponential, 
args=(mean_time_gap,), size=10000, n_reps=10000)
 
# Compute and print p-value
p_val = np.sum(reps >= d) / 10000
print('p =', p_val)



### --------------------------------------------------------
# # ------>>>>> EDA: Plotting earthquakes over time
# Plot time vs. magnitude
plt.plot(time, mags, marker='.', linestyle='none', alpha=0.1)
# Label axes and show the plot
plt.xlabel('time (year)')
plt.ylabel('magnitude')
plt.show()



### --------------------------------------------------------
# # ------>>>>> Estimates of the mean interearthquake times
# Compute mean interearthquake time
mean_dt_pre = np.mean(dt_pre)
mean_dt_post = np.mean(dt_post)
# Draw 10,000 bootstrap replicates of the mean
bs_reps_pre = dcst.draw_bs_reps(dt_pre, np.mean, size=10000)
bs_reps_post = dcst.draw_bs_reps(dt_post, np.mean, size=10000)
# Compute the confidence interval
conf_int_pre = np.percentile(bs_reps_pre, [2.5, 97.5])
conf_int_post = np.percentile(bs_reps_post, [2.5, 97.5])
# Print the results
print("""1980 through 2009
mean time gap: {0:.2f} days
95% conf int: [{1:.2f}, {2:.2f}] days""".format(mean_dt_pre, *conf_int_pre))
print("""
2010 through mid-2017
mean time gap: {0:.2f} days
95% conf int: [{1:.2f}, {2:.2f}] days""".format(mean_dt_post, *conf_int_post))



### --------------------------------------------------------
# # ------>>>>> Hypothesis test: did earthquake frequency change?
# Compute the observed test statistic
mean_dt_diff = mean_dt_pre - mean_dt_post
# Shift the post-2010 data to have the same mean as the pre-2010 data
dt_post_shift = dt_post - mean_dt_post + mean_dt_pre
 
# Compute 10,000 bootstrap replicates from arrays
bs_reps_pre = dcst.draw_bs_reps(dt_pre, np.mean, size=10000)
bs_reps_post = dcst.draw_bs_reps(dt_post_shift, np.mean, size=10000)
 
# Get replicates of difference of means
bs_reps = bs_reps_pre - bs_reps_post
# Compute and print the p-value
p_val = np.sum(bs_reps >= mean_dt_diff) / 10000
print('p =', p_val)



### --------------------------------------------------------
# # ------>>>>> How to display your analysis 
# In the last three exercises, 
# you generated a plot, 
# computed means/confidence 
# intervals, and did a 
# hypothesis test. If you were 
# to present your results to 
# others, which of the 
# following is the most 
# effective order of emphasis, 
# from greatest-to-least, you 
# should put on the respective 
# results?
# R/ 
# plot, mean/confidence interval, hypothesis test



### --------------------------------------------------------
# # ------>>>>> EDA: Comparing magnitudes before and after 2010
# Get magnitudes before and after 2010
mags_pre = mags[time < 2010]
mags_post = mags[time >= 2010]
# Generate ECDFs
plt.plot(*dcst.ecdf(mags_pre), marker='.', linestyle='none')
plt.plot(*dcst.ecdf(mags_post), marker='.', linestyle='none')
# Label axes and show plot
_ = plt.xlabel('magnitude')
_ = plt.ylabel('ECDF')
plt.legend(('1980 though 2009', '2010 through mid-2017'), loc='upper left')
plt.show()


### --------------------------------------------------------
# # ------>>>>> Quantification of the b-values
# Compute b-value and confidence interval for pre-2010
b_pre, conf_int_pre = b_value(mags_pre, mt, perc=[2.5, 97.5], n_reps=10000)
 
# Compute b-value and confidence interval for post-2010
b_post, conf_int_post = b_value(mags_post, mt, perc=[2.5, 97.5], n_reps=10000)
 
# Report the results
print("""
1980 through 2009
b-value: {0:.2f}
95% conf int: [{1:.2f}, {2:.2f}]

2010 through mid-2017
b-value: {3:.2f}
95% conf int: [{4:.2f}, {5:.2f}]
""".format(b_pre, *conf_int_pre, b_post, *conf_int_post))


### --------------------------------------------------------
# # ------>>>>> How should we do a hypothesis test on differences of the b-value?
# We wish to test the hypothesis that the b-value in Oklahoma from 1980 through 2009 
# is the same as that from 2010 through mid-2017. Which of the first five statements 
# is false? If none of them are false, select the last choice.
# You should only include earthquakes that have magnitudes above the completeness threshold. A value of 3 is reasonable.
# You should perform a permutation test because asserting a null hypothesis that the b-values are the same implicitly
# assumes that the magnitudes are identically distributed, specifically Exponentially, by the Gutenberg-Richter Law.
# A reasonable test statistic is the difference between the mean post-2010 magnitude and the mean pre-2010 magnitude.
# You do not need to worry about the fact that there were far fewer earthquakes before 2010 than there were after. 
# That is to say, there are fewer earthquakes before 2010, but sufficiently many to do a permutation test.
# You do not need to worry about the fact that the two time intervals are of different length.
# None of the above statements are false.
# R/ -> # None of the above statements are false.


### --------------------------------------------------------
# # ------>>>>> Hypothesis test: are the b-values different?
# Only magnitudes above completeness threshold
mags_pre = mags_pre[mags_pre >= mt]
mags_post = mags_post[mags_post >= mt]
 
# Observed difference in mean magnitudes: diff_obs
diff_obs = np.mean(mags_post) - np.mean(mags_pre)
 
# Generate permutation replicates: perm_reps
perm_reps = dcst.draw_perm_reps(mags_post, mags_pre, dcst.diff_of_means, size=10000)
 
# Compute and print p-value
p_val = np.sum(perm_reps < diff_obs) / 10000
print('p =', p_val)



### --------------------------------------------------------
# # # ------>>>>>What can you conclude from this analysis?
# All but one of the following constitute reasonable conclusions 
# from our analysis of earthquakes. Which one does not?
# R/Oklahoma has a smaller b-value than the Parkfield region, so 
# the Parkfield region has more earthquakes.