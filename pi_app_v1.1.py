import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

st.set_page_config(layout="wide")

st.title("π Estimation using Monte Carlo Simulation")

# --- NEW Section: What is Monte Carlo Simulation? ---
st.subheader("What is Monte Carlo Simulation?")
st.markdown("""
Monte Carlo simulation is a powerful computational technique that relies on **repeated random sampling** to obtain numerical results. Think of it like learning about something by conducting many random experiments.

**Core Idea:**
*   Instead of solving a problem with exact equations (which can be very difficult or impossible), you design a probabilistic model related to the problem.
*   You run this model many, many times, each time using random inputs drawn from specific probability distributions.
*   By analyzing the distribution or average of the outcomes from all these random runs, you can approximate the solution to the original problem.

**Why is it useful?**
Monte Carlo methods are valuable for simulating complex systems, calculating difficult integrals or probabilities, optimizing strategies, and understanding systems with inherent randomness.

**How is it used in this example?**
This app uses the Monte Carlo method to estimate the mathematical constant Pi (π). We don't calculate Pi directly using a formula like `Area = π * r²`. Instead:
1.  We define a simple geometric setup (a square and an inscribed circle).
2.  We perform a "random experiment" many times: generating a random point within the square.
3.  We check the outcome of each experiment: does the random point fall inside the circle?
4.  By looking at the *proportion* of points that fall inside the circle after many experiments, we can estimate the ratio of the circle's area to the square's area, which directly relates to π.
""")

# --- Section: How This App Estimates Pi ---
st.subheader("Estimating Pi Geometrically")
st.markdown("""
Here's how this app uses the Monte Carlo approach specifically to estimate Pi:

1.  **Imagine:** A square centered at the origin, extending from -1 to 1 on both the x and y axes (Total Area = 2 * 2 = 4).
2.  **Inscribe:** A circle with radius 1 perfectly inside this square (Area = π * 1² = π).
3.  **Random Sampling:** Generate many points (x, y) randomly and uniformly within the boundaries of the square.
4.  **Check Location:** Count how many of these points fall *inside* the circle. A point (x, y) is inside if its distance from the center (0,0) is less than or equal to the radius (1). This is checked using the condition: `x² + y² <= 1`.
5.  **Calculate Ratio:** The ratio `(Number of Points Inside Circle) / (Total Number of Points Generated)` should approximate the ratio of the areas `(Circle Area / Square Area)`, which is `π / 4`.
6.  **Estimate Pi:** Therefore, we can estimate **π ≈ 4 * (Points Inside Circle) / (Total Points)**. The more points we generate, the better this approximation tends to become.

Use the slider below to choose the number of random points to generate and click the button to run the simulation.
""")


# --- Simulation Parameters ---
st.sidebar.header("Simulation Controls")
n_points_slider = st.sidebar.slider(
    "Number of random points (log scale)",
    min_value=1,          # Corresponds to 10^1 = 10 points
    max_value=6,          # Corresponds to 10^6 = 1,000,000 points
    value=3,              # Default 10^3 = 1000 points
    step=1,
    format="10^%d"        # Display as powers of 10
)
n_points = 10**n_points_slider # Calculate actual number of points

# Use a button to trigger the simulation
run_simulation = st.sidebar.button("Run Simulation")

# Placeholders for results and plot
results_placeholder = st.empty()
plot_placeholder = st.empty()

# --- Simulation Logic and Visualization ---
def run_pi_simulation(num_points):
    """Generates points, calculates Pi estimate, and returns data for plotting."""
    if num_points <= 0:
        return np.array([]), np.array([]), np.array([]), 0, 0, 0

    # Generate random points within the [-1, 1] x [-1, 1] square
    x = np.random.uniform(-1, 1, num_points)
    y = np.random.uniform(-1, 1, num_points)

    # Calculate distance squared from origin (more efficient than sqrt)
    distance_sq = x**2 + y**2

    # Identify points inside the circle (distance_sq <= radius_sq, where radius=1)
    inside_circle = distance_sq <= 1
    points_inside = np.sum(inside_circle)
    points_total = num_points

    # Estimate Pi
    pi_estimate = 4 * points_inside / points_total if points_total > 0 else 0

    return x, y, inside_circle, pi_estimate, points_inside, points_total

def plot_simulation(x, y, inside_circle, pi_estimate, points_inside, points_total):
    """Creates the scatter plot visualization."""
    fig, ax = plt.subplots(figsize=(8, 8))

    # Check if there are points to plot
    if points_total > 0:
        # Scatter plot points: blue if inside, red if outside
        ax.scatter(x[inside_circle], y[inside_circle], color='blue', alpha=0.5, s=5, label='Inside Circle')
        ax.scatter(x[~inside_circle], y[~inside_circle], color='red', alpha=0.5, s=5, label='Outside Circle')

        # Add text for the estimate
        ax.text(-1.05, 1.05, f"Points Inside: {points_inside:,}\nTotal Points: {points_total:,}\nEstimate for π: {pi_estimate:.6f}\nActual π: {math.pi:.6f}",
                verticalalignment='top', horizontalalignment='left',
                bbox=dict(boxstyle='round,pad=0.5', fc='wheat', alpha=0.8))
        ax.legend(loc='upper right')
    else:
         ax.text(0, 0, "No points generated", horizontalalignment='center', verticalalignment='center')


    # Draw the circle and square boundaries
    circle = plt.Circle((0, 0), 1, color='green', fill=False, linewidth=2, label='Circle Boundary (r=1)')
    square = plt.Rectangle((-1, -1), 2, 2, color='black', fill=False, linewidth=2, label='Square Boundary')
    ax.add_patch(circle)
    ax.add_patch(square)

    # Plot settings
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel("X-coordinate")
    ax.set_ylabel("Y-coordinate")
    ax.set_title(f"Monte Carlo Estimation of Pi (N = {points_total:,})")
    ax.grid(True, linestyle='--', alpha=0.6)

    # Only add legend if there are points
    if points_total > 0:
        handles, labels = ax.get_legend_handles_labels()
        # Filter out the circle/square from the main legend if desired, or just show all
        ax.legend(handles=handles, labels=labels, loc='upper right')


    plt.tight_layout()
    return fig


# --- App Execution ---
if run_simulation:
    # Run the simulation
    x_coords, y_coords, is_inside, estimate, inside_count, total_count = run_pi_simulation(n_points)

    # Display results
    results_placeholder.markdown(f"""
    ### Simulation Results:
    *   **Total points generated:** {total_count:,}
    *   **Points inside the circle:** {inside_count:,}
    *   **Estimated value of π:** `{estimate:.8f}`
    *   **Actual value of π:** `{math.pi:.8f}`
    *   **Difference:** `{abs(estimate - math.pi):.8f}`
    """)

    # Create and display the plot
    fig = plot_simulation(x_coords, y_coords, is_inside, estimate, inside_count, total_count)
    plot_placeholder.pyplot(fig)

else:
    # Show initial message or previous results if desired
    results_placeholder.info("Adjust the slider and click 'Run Simulation' in the sidebar to start.")
    # Optionally clear the plot or show a default empty plot
    plot_placeholder.empty()

    # --- Author Information --- <--- INSERT HERE
st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    **Author:** Chris Hopwood  
    **Email:** [chopwood24@gmail.com](mailto:chopwood24@gmail.com)
    """
)
# --- REMOVED Section explaining MCMC connection ---
# (The previous MCMC explanation block is deleted from here)