from src.config import *
from src.functions import *


def LaTeX(truefalse: bool) -> None:
    """Toggle LaTeX rendering in matplotlib.

    Args:
        truefalse: If True, enable LaTeX rendering with sans-serif font.
            If False, disable LaTeX rendering.

    Returns:
        None
    """
    if truefalse:
        plt.rcParams.update({
            "text.usetex": True,
            "font.family": "sans-serif",
            "font.sans-serif": "avant"
        })
    else:
        plt.rcParams.update({
            "text.usetex": False,
            "font.sans-serif": "DejaVu Sans",
        })
    return None


def plotStreamFunction(psi: np.ndarray, figsize: float, dpi: int) -> None:
    """Plot the stream function.

    Args:
        psi: 2D array (N x N) containing the stream function values.
        figsize: Size of the figure in inches.
        dpi: Dots per inch for the figure resolution.

    Returns:
        None
    """
    r = np.max([-np.min(psi), np.max(psi)])
    fig, ax = plt.subplots(
        1,1,
        figsize=(figsize,figsize),
        dpi=dpi
        )
    ax.set_title(r"Random generated stream function $\psi$")
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    im1 = ax.imshow(psi, cmap=cmasher.prinsenvlag, origin='lower', vmin=-r, vmax=r)
    cbar = fig.colorbar(im1,shrink=0.8)
    cbar.set_label(r"$\psi$",rotation=0,size=12)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.contour(psi, levels=30, origin='lower', cmap=cmasher.prinsenvlag, vmin=-1.5*r, vmax=1.5*r)
    plt.show()

def plotVelocityfields(vx: np.ndarray, vy: np.ndarray, figsize: float, dpi: int) -> None:
    """Plot the x, y components and magnitude of the velocity field in one figure.

    Args:
        vx: 2D array with x-component of velocity.
        vy: 2D array with y-component of velocity.
        figsize: Size of the figure in inches (width will be 3*figsize for subplots).
        dpi: Dots per inch for the figure resolution.

    Returns:
        None
    """
    fig, axes = plt.subplots(1, 3, figsize=(figsize * 3, figsize), dpi=dpi)
    fig.suptitle(r"Velocity fields $\vec{\mathbf{u}}=(v_x, v_y)$ derived from stream function $\psi$", fontsize=15, fontweight='bold')
    colorbar_size = 0.8
    
    # Plot u
    r_vx = np.max([-np.min(vx), np.max(vx)])
    im_vx = axes[0].imshow(vx, cmap=cmasher.waterlily, origin='lower', vmin=-r_vx, vmax=r_vx)
    axes[0].set_title(r"$x-$direction")
    axes[0].set_xlabel(r"$x$")
    axes[0].set_ylabel(r"$y$")
    axes[0].set_xticks([])
    axes[0].set_yticks([])
    cbar_vx = fig.colorbar(im_vx, ax=axes[0], shrink=colorbar_size)
    cbar_vx.set_label(r"$v_x$", rotation=0, size=12)
    
    # Plot v
    r_vy = np.max([-np.min(vy), np.max(vy)])
    im_vy = axes[1].imshow(vy, cmap=cmasher.waterlily, origin='lower', vmin=-r_vy, vmax=r_vy)
    axes[1].set_title(r"$y-$direction")
    axes[1].set_xlabel(r"$x$")
    axes[1].set_ylabel(r"$y$")
    axes[1].set_xticks([])
    axes[1].set_yticks([])
    cbar_vy = fig.colorbar(im_vy, ax=axes[1], shrink=colorbar_size)
    cbar_vy.set_label(r"$v$", rotation=0, size=12)
    
    # Plot absolute velocity
    abs_vel = np.sqrt(vx**2 + vy**2)
    im_abs = axes[2].imshow(abs_vel, cmap=cmasher.ocean, origin='lower', vmin=0)
    axes[2].set_title(r"Absolute amplitude")
    axes[2].set_xlabel(r"$x$")
    axes[2].set_ylabel(r"$y$")
    axes[2].set_xticks([])
    axes[2].set_yticks([])
    cbar_abs = fig.colorbar(im_abs, ax=axes[2], shrink=colorbar_size)
    cbar_abs.set_label(r"$|\vec{\mathbf{u}}|$", rotation=0, size=12)
    
    plt.tight_layout()
    plt.show()

def plotVorticity(vx: np.ndarray, vy: np.ndarray, omega: np.ndarray, figsize: float, dpi: int) -> None:
    """Create a stream plot overlaid with the vorticity field.

    Args:
        vx: 2D array with x-component of velocity.
        vy: 2D array with y-component of velocity.
        omega: 2D vorticity field to display as a background image.
        figsize: Size of the figure in inches.
        dpi: Dots per inch for the figure resolution.

    Returns:
        None
    """
    fig, ax = plt.subplots(1, 1, figsize=(figsize, figsize), dpi=dpi)
    y, x = np.mgrid[0:vx.shape[0], 0:vx.shape[1]]

    r = np.max([-np.min(omega), np.max(omega)])
    im = ax.imshow(omega, origin='lower', cmap=cmasher.prinsenvlag, vmin=-r, vmax=r)
    ax.streamplot(
        x, y, 
        vx, vy, 
        density=3,
        color='k',#np.sqrt(vx**2 + vy**2), 
        # cmap=cmasher.ocean,
        linewidth=0.5,
        arrowsize = 0.5,
        arrowstyle='fancy'
        )
    ax.set_title(r"Vorticity $\omega$")
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")
    ax.set_xticks([])
    ax.set_yticks([])
    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label(r"$\omega$", rotation=0, size=12)
    plt.show()

def plotOkuboWeissField(Q: np.ndarray, vx: np.ndarray, vy: np.ndarray, figsize: float, dpi: int) -> None:
    """Plot the Okubo–Weiss field with overlaid velocity streamplots, showing vorticity and strain dominated regions separately.

    Args:
        Q: 2D Okubo–Weiss scalar field.
        vx: 2D array with x-component of velocity.
        vy: 2D array with y-component of velocity.
        figsize: Size of the figure in inches (width will be 2*figsize for subplots).
        dpi: Dots per inch for the figure resolution.

    Returns:
        None
    """
    fig, axes = plt.subplots(1, 2, figsize=(figsize * 2, figsize), dpi=dpi)
    fig.suptitle(r"Okubo-Weiss field $Q(x,y)$", fontsize=14)
    y, x = np.mgrid[0:vy.shape[0], 0:vy.shape[1]]
    
    # Left plot: Vorticity-dominated regions (Q < 0)
    axes[0].streamplot(
        x, y,
        vx, vy,
        density=2,
        color='dimgray',
        linewidth=0.5,
        arrowsize=0.5,
        arrowstyle='fancy',
    )
    vorticity_part = (Q < 0) * Q
    im0 = axes[0].imshow(vorticity_part, cmap=cmasher.arctic_r, origin='lower')
    axes[0].set_title(r"Vorticity-dominated ($Q < 0$)")
    axes[0].set_xlabel(r"$x$")
    axes[0].set_ylabel(r"$y$")
    axes[0].set_xticks([])
    axes[0].set_yticks([])
    cbar0 = fig.colorbar(im0, ax=axes[0], shrink=0.8)
    cbar0.set_label(r"$Q$", rotation=0, size=12)
    
    # Right plot: Strain-dominated regions (Q > 0)
    axes[1].streamplot(
        x, y,
        vx, vy,
        density=2,
        color='dimgray',
        linewidth=0.5,
        arrowsize=0.5,
        arrowstyle='fancy',
    )
    strain_part = (Q > 0) * Q
    im1 = axes[1].imshow(strain_part, cmap=cmasher.jungle, origin='lower')
    axes[1].set_title(r"Strain-dominated ($Q > 0$)")
    axes[1].set_xlabel(r"$x$")
    axes[1].set_ylabel(r"$y$")
    axes[1].set_xticks([])
    axes[1].set_yticks([])
    cbar1 = fig.colorbar(im1, ax=axes[1], shrink=0.8)
    cbar1.set_label(r"$Q$", rotation=0, size=12)
    
    plt.tight_layout()
    plt.show()


def plotNumericalChecks(psi: np.ndarray, vx: np.ndarray, vy: np.ndarray, figsize: float, dpi: int) -> None:
    """Plot numerical checks that verify velocity/stream relationships and continuity on a log scale.

    Three checks are displayed (absolute values):
    1. Continuity: |∇·u| (should be close to zero for incompressible flow)
    2. Stream function check 1: |u·∇ψ| (should be close to zero for stream function derived velocities)
    3. Stream function check 2: ||u|² - |∇ψ|²| (checks equality of magnitudes)

    Args:
        psi: 2D stream function array.
        vx: 2D array with x-component of velocity.
        vy: 2D array with y-component of velocity.
        figsize: Size of the figure in inches (width will be 3*figsize for subplots).
        dpi: Dots per inch for the figure resolution.

    Returns:
        None
    """
    # Continuity check
    continuity = np.abs(ddx(vx) + ddy(vy)) + 1e-15
    # Stream function checks
    A = np.abs(vx * ddx(psi) + vy * ddy(psi)) + 1e-15
    B = np.abs(vx**2 + vy**2 - ddx(psi)**2 - ddy(psi)**2) + 1e-15
    
    fig, axes = plt.subplots(1, 3, figsize=(figsize * 3, figsize), dpi=dpi)
    fig.suptitle(r"Numerical Checks", fontsize=14)
    colormap = cmasher.neutral
    # Plot Continuity
    im_cont = axes[0].imshow(continuity, cmap=colormap, origin='lower', norm=LogNorm(vmin=1e-15))
    axes[0].set_title(r"$|\nabla \cdot \vec{\mathbf{u}}|=0$")
    axes[0].set_xlabel(r"$x$")
    axes[0].set_ylabel(r"$y$")
    axes[0].set_xticks([])
    axes[0].set_yticks([])
    cbar_cont = fig.colorbar(im_cont, ax=axes[0], shrink=0.6)
    cbar_cont.set_label(r"$|\nabla \cdot \vec{\mathbf{u}}|$", rotation=0, size=12)
    
    # Plot A
    im_A = axes[1].imshow(A, cmap=colormap, origin='lower', norm=LogNorm(vmin=1e-15))
    axes[1].set_title(r"$|\vec{\mathbf{u}} \cdot \nabla\psi| = 0$")
    axes[1].set_xlabel(r"$x$")
    axes[1].set_ylabel(r"$y$")
    axes[1].set_xticks([])
    axes[1].set_yticks([])
    cbar_A = fig.colorbar(im_A, ax=axes[1], shrink=0.6)
    cbar_A.set_label(r"$|\vec{\mathbf{u}} \cdot \nabla\psi|$", rotation=0, size=12)
    
    # Plot B
    im_B = axes[2].imshow(B, cmap=colormap, origin='lower', norm=LogNorm(vmin=1e-15))
    axes[2].set_title(r"$||\vec{\mathbf{u}}|^2 - |\nabla\psi|^2|=0$")
    axes[2].set_xlabel(r"$x$")
    axes[2].set_ylabel(r"$y$")
    axes[2].set_xticks([])
    axes[2].set_yticks([])
    cbar_B = fig.colorbar(im_B, ax=axes[2], shrink=0.6)
    cbar_B.set_label(r"$||\vec{\mathbf{u}}|^2 - |\nabla\psi|^2|$", rotation=0, size=12)
    
    plt.tight_layout()
    plt.show()
