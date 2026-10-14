%% BAM ML & Communication Skills proposal class (clean-mode layout
%% matched to the official annotated template PDF styling).
%% If Blackboard/Overleaf gives you the official bam-proposal.cls,
%% replace THIS file with that one (keep main.tex / figures / bib).
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{bam-proposal}[2026/10/11 BAM ML proposal class (template-matched)]
\newif\ifannotated
\DeclareOption{annotated}{\annotatedtrue}
\DeclareOption{clean}{\annotatedfalse}
\ExecuteOptions{clean}
\ProcessOptions\relax
\LoadClass[11pt,a4paper]{article}

\RequirePackage[T1]{fontenc}
\RequirePackage[utf8]{inputenc}
\RequirePackage{lmodern}
\RequirePackage{microtype}
\RequirePackage[left=1.7cm,right=1.7cm,top=1.6cm,bottom=2.0cm]{geometry}
\RequirePackage{setspace}
\RequirePackage{xcolor}
\RequirePackage{graphicx}
\RequirePackage{booktabs}
\RequirePackage{tabularx}
\RequirePackage{array}
\RequirePackage{amsmath,amssymb}
\RequirePackage{titlesec}
\RequirePackage{fancyhdr}
\RequirePackage{hyperref}
\RequirePackage[numbers,sort&compress]{natbib}
\RequirePackage{caption}
\RequirePackage{enumitem}
\setlist{nosep,leftmargin=*}

%% Colours sampled from the official annotated template PDF
\definecolor{BAMblue}{HTML}{080886}
\definecolor{BAMgray}{HTML}{5F6670}
\definecolor{BAMboxborder}{HTML}{7A9BB8}
\definecolor{BAMboxfill}{HTML}{EEF3F8}
\colorlet{BAMaccent}{BAMblue}

\hypersetup{colorlinks=true,linkcolor=BAMblue,citecolor=BAMblue,urlcolor=BAMblue}

\newcommand{\BAMtitle}[1]{\gdef\@BAMtitle{#1}}
\newcommand{\BAMteam}[1]{\gdef\@BAMteam{#1}}
\newcommand{\BAMcourse}[1]{\gdef\@BAMcourse{#1}}
\newcommand{\BAMacademicyear}[1]{\gdef\@BAMacademicyear{#1}}
\newcommand{\BAMsubmissiondate}[1]{\gdef\@BAMsubmissiondate{#1}}
\newcommand{\BAMbibliographystyle}[1]{\gdef\@BAMbibliographystyle{#1}}
\newcommand{\BAMbibliographyfile}[1]{\gdef\@BAMbibliographyfile{#1}}

\BAMtitle{}
\BAMteam{}
\BAMcourse{Machine Learning \& Communication Skills}
\BAMacademicyear{2026--2027}
\BAMsubmissiondate{11 October 2026, 23:59 Madrid time}
\BAMbibliographystyle{plainnat}
\BAMbibliographyfile{references}

\titleformat{\section}
  {\normalfont\large\bfseries\color{BAMblue}}
  {\thesection}{0.6em}{}
\titlespacing*{\section}{0pt}{1.1em}{0.45em}

\pagestyle{fancy}
\fancyhf{}
\fancyfoot[C]{\small\thepage}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
\fancypagestyle{plain}{%
  \fancyhf{}%
  \fancyfoot[C]{\small\thepage}%
  \renewcommand{\headrulewidth}{0pt}%
}

\newcommand{\makeproposalheader}{%
  \noindent
  \begin{minipage}[t]{0.78\textwidth}
    {\footnotesize\bfseries IE UNIVERSITY\,|\,SCHOOL OF SCIENCE \& TECHNOLOGY\par}
    \vspace{0.35em}
    {\large\bfseries\color{BAMblue} Machine Learning \& Communication Skills -- Project Proposal\par}
    \vspace{0.55em}
    {\Large\bfseries\@BAMtitle\par}
  \end{minipage}%
  \hfill
  \begin{minipage}[t]{0.18\textwidth}
    \raggedleft
    \IfFileExists{figures/ie-logo.png}{%
      \includegraphics[width=1.55cm]{figures/ie-logo.png}%
    }{}%
  \end{minipage}\par
  \vspace{0.85em}
  \noindent
  \begin{tabular}{@{}>{\bfseries}p{0.26\textwidth}@{\hspace{0.6em}}p{0.70\textwidth}@{}}
    Team: & \@BAMteam \\[0.15em]
    Course: & \@BAMcourse \\[0.15em]
    Academic year: & \@BAMacademicyear \\[0.15em]
    Submission deadline: & \@BAMsubmissiondate \\[0.15em]
    Text limit: & 2 pages; figures excluded from the page count \\
  \end{tabular}\par
  \vspace{0.7em}
  \ifannotated
    \noindent
    \fcolorbox{black}{white}{%
      \parbox{0.96\textwidth}{%
        \centering\bfseries
        ANNOTATED GUIDANCE COPY.\\[0.25em]
        {\color{red}Change \texttt{annotated} to \texttt{clean} before preparing the submitted proposal.}%
      }%
    }\par
    \vspace{0.6em}
  \fi
}

\newcommand{\BAMannotationnotice}{}
\newcommand{\annotation}[1]{\ifannotated\noindent{\color{BAMgray}\footnotesize #1}\par\medskip\fi}
\newcommand{\placeholder}[1]{#1}

\newcommand{\BAMprintbibliography}{%
  \bibliographystyle{\@BAMbibliographystyle}%
  \bibliography{\@BAMbibliographyfile}%
}

\setlength{\parskip}{0.32em}
\setlength{\parindent}{0pt}
\setstretch{1.05}
\captionsetup{font=small,labelfont=bf}
\renewcommand{\refname}{References}
