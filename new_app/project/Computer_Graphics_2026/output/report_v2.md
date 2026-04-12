\documentclass[12pt,a4paper]{article}
\usepackage{float}
\usepackage{graphicx}
\usepackage[margin=1.1cm]{geometry}
\usepackage{longtable}
\usepackage{booktabs}
\usepackage{array}
\usepackage{ragged2e}
\usepackage{pdflscape}
\usepackage{caption}

% Table settings
\renewcommand{\arraystretch}{1.32}
\setlength{\tabcolsep}{5pt}

\title{Assignment 1}
\author{Daris Dzakwan Hoesien}
\date{April 7, 2026}

\begin{document}

\maketitle

\section{Introduction}
This project demonstrates the implementation and testing of Tasks 1–4 from the Computer Graphics Programming Assignment 1. The delivered program renders a colored tetrahedron and was extended to include a continuous rotation around the X axis, an Euler-angle based camera controlled with the mouse, and keyboard movement for free navigation. Small compatibility fixes were applied so the program runs on a macOS OpenGL context.

Environment and setup
The environment is adjusted to author's environment and version of Python 3.10.11, that requires PyOpenGL, PyOpenGL\_accelerate and PyGLM, and the system FreeGLUT library (installable via Homebrew).

When first running the provided code, shader lookup and GLSL version mismatches prevented the scene from compiling. To make the program robust across environments, the shader loader was modified to build absolute paths from the script directory and the shaders were adapted to GLSL 1.20 (attribute/varying/gl\_FragColor) so they compile on the compatibility GL profile commonly provided on macOS. The program now reliably compiles, links, and uses the vertex and color buffers to draw the tetrahedron.
\section{Task}
\subsection{Task 1 — initial (unmodified) scene}
\begin{figure}[H]
    \centering
    % Replace the filename below with the screenshot taken from the original, unmodified run
    \includegraphics[width=0.40\linewidth]{images/ComputerGraphics/Screenshot_initial.png}
    \caption{Task 1 — Initial scene (original program run before modifications). This image documents the baseline tetrahedron rendering used for all subsequent tasks.}
\end{figure}

\subsection{Task 2 — continuous X-axis rotation}
\begin{figure}[H]
    \centering
    \includegraphics[width=0.30\linewidth]{images/ComputerGraphics/Screenshot 2026-03-31 at 19.55.14.png}
    \caption{Task 2 — Rotating tetrahedron (single frame). Rotation is produced by applying glm.rotate(angle, (1,0,0)) to the model matrix where angle is derived from elapsed time.}
\end{figure}

\subsection{Task 3 — Euler-angle camera (mouse look)}
\begin{figure}[H]
    \centering
    \includegraphics[width=0.30\linewidth]{images/ComputerGraphics/Screenshot 2026-03-31 at 19.55.17.png}
    \caption{Task 3 — Camera moved via mouse-look (yaw / pitch). The view matrix is computed with glm.lookAt using direction, right and up derived from yaw/pitch.}
\end{figure}

\subsection{Task 4 — keyboard movement}
\begin{figure}[H]
    \centering
    \includegraphics[width=0.30\linewidth]{images/ComputerGraphics/Screenshot 2026-03-31 at 19.55.19.png}
    \caption{Task 4 — Camera translated with keyboard (W/S/A/D/E/R). The screenshot shows the camera at a different location indicating movement along forward/right/up vectors.}
\end{figure}

\section{Changelog (code-level summary)}
\begin{itemize}
  \item CG\_assignment1.py
    \begin{itemize}
      \item Fixed shader path resolution: read shader files using absolute path relative to script directory to avoid runtime lookup failures.
      \item Adjusted shaders to GLSL 1.20 compatibility (attribute / varying / gl\_FragColor) for macOS compatibility.
      \item Added continuous model rotation around the X axis using glm.rotate with elapsed time as angle source.
      \item Implemented Euler-angle camera (yaw/pitch) and computed view matrix with glm.lookAt.
      \item Added keyboard movement handlers for W/S/A/D/E/R (keys handled as bytes) to update camera position.
      \item Uploaded and bound vertex and color VBOs; ensured attribute locations match shader bindings.
    \end{itemize}
  \item utils/ (if applicable)
    \begin{itemize}
      \item Minor compatibility fixes to window/context helpers (GL context and projection update on resize).
    \end{itemize}
\end{itemize}

\section{What I returned}
Submitted files included with this report:
\begin{itemize}
  \item Assignment code: \texttt{CG\_assignment1.py}
  \item Shaders: \texttt{shaders/vertex\_shader.glsl}, \texttt{shaders/fragment\_shader.glsl}
  \item Report PDF: \texttt{output/report\_v2.pdf}
  \item Screenshots: \texttt{images/ComputerGraphics/*.png}
  \item (Optional) Streamlit comparison page: \texttt{new\_app/pages/1\_code\_comparison.py}
\end{itemize}

\section{Reproduction steps (macOS)}
Open Terminal in the project folder and run:
\begin{verbatim}
# install FreeGLUT if missing
brew install freeglut

# create virtualenv and install required Python packages
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install PyOpenGL PyOpenGL_accelerate PyGLM

# run the program (from project folder containing CG_assignment1.py)
python3 CG_assignment1.py
\end{verbatim}

Notes:
\begin{itemize}
  \item Python version used for testing: 3.10.x
  \item If you need the true "initial" screenshot but only have the modified code, temporarily restore the original CG\_assignment1.py (or check it out from version control), run the original program and capture the window.
  \item Use the provided Streamlit code comparison page (\texttt{new\_app/pages/1\_code\_comparison.py}) to generate a quick change report / diff between original and modified files.
\end{itemize}

\section{Results and observations}
The program renders a smoothly shaded tetrahedron with interpolated vertex colours, supports a continuous rotation around the local X axis, and provides an Euler-angle mouse-look plus keyboard navigation (W/S/A/D/E/R). The screenshots below are representative frames used to verify each assignment task and to document camera positions used during testing.

Screenshots (task-mapped)
[[Screenshot 2026-03-31 at 19.55.14]]
Screenshot — Task 2 (rotation)
- Description: A single-frame capture showing the tetrahedron rotated about its local X axis. Rotation is applied to the model matrix using glm.rotate(angle, (1,0,0)) where angle is computed from elapsed time. This confirms the continuous rotation update is active.

[[Screenshot 2026-03-31 at 19.55.40]]
Screenshot — Task 3 (mouse-look / Euler camera)
- Description: Camera rotated via mouse drag to change yaw and pitch. The view matrix is computed with glm.lookAt using direction, right and up vectors derived from yaw/pitch. This view demonstrates correct camera orientation and that mouse input updates the view transform.

[[Screenshot 2026-03-31 at 19.55.58]]
Screenshot — Task 4 (keyboard translation)
- Description: Camera moved via keyboard (W/S/A/D/E/R). The frame shows the camera at a translated position relative to the scene, validating movement along forward/right/up axes. Keys are handled as bytes in the GLUT callback to ensure correct input on macOS.

[[Screenshot_initial]]
Screenshot — Task 1 (initial, unmodified scene)
- Description: The baseline scene captured from the original (unmodified) program run. This image documents the default tetrahedron rendering used before applying shader/path compatibility fixes and feature additions.

How to reproduce these views quickly (macOS)
- Run the program from the project folder:
  - python3 CG_assignment1.py
- Controls:
  - Mouse drag = yaw/pitch look
  - W/S/A/D/E/R = move forward/back/left/right/up/down
- Capture a screenshot of the running window (example, run from Terminal):
  - screencapture -l $(osascript -e 'tell app "System Events" to get the unix id of (first process whose frontmost is true)') images/ComputerGraphics/Screenshot_initial.png
  - Or use the Grab tool / Cmd-Shift-4 to select the window.

Notes
- Ensure FreeGLUT and Python dependencies (PyOpenGL, PyOpenGL_accelerate, PyGLM) are installed before running.
- If the original unmodified program is not available, temporarily restore the original file from version control, run and capture the Task 1 screenshot, then re-apply

