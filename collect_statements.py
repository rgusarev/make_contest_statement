# This Python file uses the following encoding: cp1251

'''
1. Read the serve.cfg. 
2. Get the path: <problem_dir> for abstract task + <problem_dir> for each task
3. Create a set of contest paths
4. Update all individual statements for tasks in each contest.
5. Get individual statements and create one statement file for thi contest
'''

import platform
import os

EJUDGE_HOME = "/home/judges/"

statement_header = r"""
\documentclass[a4paper]{article}
\pagestyle{empty}
\usepackage[T2A]{fontenc}
\usepackage[cp1251]{inputenc}
\usepackage[russian]{babel}
\usepackage{amssymb}
\usepackage{amsmath}
\usepackage{tabularx}
\usepackage{listings}
\usepackage{graphicx}
\usepackage{cmap}

\setlength{\baselineskip}{5em}
\setlength{\textwidth}{19cm}
\setlength{\textheight}{29cm}
\setlength{\oddsidemargin}{-17mm}
\setlength{\evensidemargin}{-17mm}
\setlength{\topmargin}{-31mm}

\renewcommand{\theenumi}{\Alph{enumi}}

\newcommand{\comptask}{\stepcounter{enumi}\theenumi$^*$}
\newcommand{\imptask}{\stepcounter{enumi}\theenumi$^\circ$}

\makeatletter

\def\verbsettings{\topsep=0pt\partopsep=0pt
\parsep=2pt\parskip=0pt\parindent=0pt\@totalleftmargin=0pt
\renewcommand{\baselinestretch}{0.8}\hsize=}

\def\myAlpha#1{{\@tempcnta=\csname c@#1\endcsname\relax
\advance\@tempcnta by -1\relax\@tempcntb=\@tempcnta\relax
\divide\@tempcntb by 26\relax\multiply\@tempcntb by 26\relax
\advance\@tempcnta by -\@tempcntb\relax\divide\@tempcntb by 26\relax
\advance\@tempcnta by 65\relax
%\ifnum\@tempcntb>0\advance\@tempcntb by 64\relax\char\@tempcntb\fi
\ifnum\@tempcntb>0Z\fi
\char\@tempcnta}} % macro dlya odno- i dvuznachnykh bukvennykh napisanij

\def\@listi{} \def\@listI{}
\itemsep=7pt
%\parskip=0pt \topsep=0pt \partopsep=0pt \parsep=0pt % ubivaem vse vertikalnye otstupy

\def\theenumi{\myAlpha{enumi}} % enumi --- eto schyotchik pervogo urovnya enumerate
	% theenumi --- tak budet pechatat'sya znachenie schyotchika
\def\labelenumi{\theenumi.} % tak dobavlyaetsya znak prepinaniya

\makeatother

\begin{document}
\Large
\center\textbf{Тут заголовок}
\flushleft
\large
\bigskip
\par Тут описание задач.
\par Тут продолжение описания задач.

\begin{enumerate}
\setlength{\itemsep}{7pt}

"""
statement_footer = r"""

\end{enumerate}
\end{document}
"""


def update_all_statements(path):
    '''
    Update all single task statements from given contest path
    '''
    try:
        s = open(f"{EJUDGE_HOME}{dir_sep}{path}{dir_sep}_statement{dir_sep}statemen.tex", encoding="cp1251").read()
        tasks = s.split("\item\emph")[1:]
        tasks = ["\item\emph" + prob_text for prob_text in tasks]
        tasks[-1] = tasks[-1][:tasks[-1].rfind('\end{enum')]
    except Exception as error:
        print("Something got wrong, below are details:")
        print(error)

    all_letters = list(ascii_uppercase) + ['Z' + let for let in ascii_uppercase]
    subfolders = sorted([ f.path for f in os.scandir("problems") if f.is_dir() ])

    for k in range(min(len(all_letters), len(subfolders))):
        with open(subfolders[k] + f"{dir_sep}statement.tex", 'w', encoding="cp1251") as f:
            f.write(tasks[k])
            print(f"Task statement for {all_letters[k]} is in the folder {subfolders[k]}")


try:
    dir_sep = '/'
    if platform.system == 'Windows':
        dir_sep = '\\'

    #  reading serve.conf and list of problem's folders
    dirs = []
    with open(f"conf{dir_sep}serve.cfg") as conf:
        for line in conf:
            if line.startswith("problem_dir") and 'home' not in line:
                dirs.append(line[15:-2])

    statement = ""
    standard_home = "/home/judges/problems/"
    for d in dirs:
        with open(standard_home + d + f"{dir_sep}statement.tex", encoding="1251") as f:
            s = f.read()
            statement += ("\n" + s + "\n")


    with open("collected.tex", 'w', encoding="cp1251") as f:
        f.write(statement_header + statement + statement_footer)
except Exception as err:
    print("Something got wrong, see details below")
    print(err)