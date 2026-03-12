import random
import numpy as np
import matplotlib.pyplot as plt


def score_to_maze_size(score: float, min_size: int = 10, max_size: int = 30) -> int:
    """
    Convert a normalized food access score (0 to 1) into an odd maze size.

    Higher score -> larger maze.
    """
    score = max(0.0, min(1.0, float(score)))
    size = int(min_size + score * (max_size - min_size))

    # keep size odd for cleaner maze generation
    if size % 2 == 0:
        size += 1

    return size


def generate_maze(width: int, height: int, seed: int | None = None) -> np.ndarray:
    """
    Generate a maze using recursive backtracking (DFS).

    Returns a 2D numpy array:
    - 1 = wall
    - 0 = path
    """
    if seed is not None:
        random.seed(seed)

    # ensure odd dimensions
    if width % 2 == 0:
        width += 1
    if height % 2 == 0:
        height += 1

    maze = np.ones((height, width), dtype=int)

    def carve_passages(x: int, y: int) -> None:
        directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 < nx < width - 1 and 0 < ny < height - 1 and maze[ny, nx] == 1:
                # carve wall between current cell and next cell
                maze[y + dy // 2, x + dx // 2] = 0
                maze[ny, nx] = 0
                carve_passages(nx, ny)

    # start point
    start_x, start_y = 1, 1
    maze[start_y, start_x] = 0
    carve_passages(start_x, start_y)

    # entrance and exit
    maze[0, 1] = 0
    maze[height - 1, width - 2] = 0

    return maze


def add_solution_path(maze: np.ndarray) -> list[tuple[int, int]]:
    """
    Solve the maze using DFS and return the solution path as a list of (row, col).
    Entrance is assumed at (0,1), exit at (height-1,width-2).
    """
    height, width = maze.shape
    start = (0, 1)
    goal = (height - 1, width - 2)

    stack = [(start, [start])]
    visited = set()

    while stack:
        (r, c), path = stack.pop()

        if (r, c) == goal:
            return path

        if (r, c) in visited:
            continue

        visited.add((r, c))

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < height
                and 0 <= nc < width
                and maze[nr, nc] == 0
                and (nr, nc) not in visited
            ):
                stack.append(((nr, nc), path + [(nr, nc)]))

    return []


def render_maze(
    maze: np.ndarray,
    solution_path: list[tuple[int, int]] | None = None,
    title: str | None = None,
    figsize: tuple[int, int] = (8, 8),
):
    """
    Render the maze with matplotlib.

    Walls are dark, paths are light.
    If solution_path is provided, overlay it.
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.imshow(maze, cmap="binary")

    if solution_path:
        ys = [r for r, c in solution_path]
        xs = [c for r, c in solution_path]
        ax.plot(xs, ys, linewidth=2)

    if title:
        ax.set_title(title, fontsize=14, pad=12)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    plt.tight_layout()
    return fig


def generate_maze_from_score(
    score: float,
    show_solution: bool = False,
    seed: int | None = None,
):
    """
    Convenience wrapper:
    score -> maze size -> maze -> optional solution -> matplotlib figure
    """
    size = score_to_maze_size(score)
    maze = generate_maze(size, size, seed=seed)
    solution = add_solution_path(maze) if show_solution else None
    fig = render_maze(
        maze,
        solution_path=solution,
        title=f"Food Access Maze (score={score:.2f}, size={size}x{size})",
    )
    return fig, maze
