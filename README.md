# GameOfCats-Naradha
Python based game to simulate cats in a 2d space. The user can add cats into a custom 2d csv based map. The code simulates cats hunger, thirst, fatigue and stress. It also includes cat to cat interactions such as fighting, mating and parent-child relationships. Please read the readme before attempting to play it.

README FOR Game Of Cats By W.M.Naradha

## Version information

<11th Octomber 2021> - First Stable Version.


## Dependencies

tkinter (tk)
matplotlib
numpy 
threading
math
random

## Contents:

The file map shows all the contents in the program, the plots in the respective results folders are removed.

File Map:
GOC_CreatedByNaradha
```
├── README
├── setup.sh
├── GameOfCats_W.M.Naradha_20469160.pdf
├── inputs
│   ├── terrain1.csv
│   ├── terrain2.csv
│   ├── terrain3.csv
│   └── terrain4.csv
├── object_py
│   ├── bucket.py
│   ├── cat.py
│   ├── file_manager.py
│   ├── goc_gui.py
│   ├── landmarks.py
│   └── simulation.py
└── saves
    ├── CD_Sim
    │   ├── CD_Sim20211008-120740
    │   │   ├── CD_Simlog.csv
    │   │   ├── CD_Sim-plots-20211008-120741
    │   │   └── plotter.py
    │   ├── CD_Sim20211008-121850
    │   │   ├── CD_Simlog.csv
    │   │   ├── CD_Sim-plots-20211008-121851
    │   │   └── plotter.py
    │   ├── CD_Sim20211008-123812
    │   │   ├── CD_Simlog.csv
    │   │   ├── CD_Sim-plots-20211008-123813
    │   │   └── plotter.py
    │   ├── CD_Sim20211008-124416
    │   │   ├── CD_Simlog.csv
    │   │   ├── CD_Sim-plots-20211008-124417
    │   │   └── plotter.py
    │   └── CD_Sim.csv
    ├── CLI
    │   ├── CLI20211008-124744
    │   │   ├── CLIlog.csv
    │   │   ├── CLI-plots-20211008-124744
    │   │   └── plotter.py
    │   ├── CLI20211008-125254
    │   │   ├── CLIlog.csv
    │   │   ├── CLI-plots-20211008-125256
    │   │   └── plotter.py
    │   └── CLI.csv
    ├── CtoC_extensive
    │   ├── CtoC_extensive20211010-030521
    │   │   ├── CtoC_extensivelog.csv
    │   │   ├── CtoC_extensive-plots-20211010-030538
    │   │   └── plotter.py
    │   └── CtoC_extensive.csv
    ├── CtoC_Fights
    │   ├── CtoC_Fights20211010-031940
    │   │   ├── CtoC_Fightslog.csv
    │   │   └── CtoC_Fights-plots-20211010-031941
    │   └── CtoC_Fights.csv
    ├── CtoC_Stress
    │   ├── CtoC_Stress20211008-154639
    │   │   ├── CtoC_Stresslog.csv
    │   │   ├── CtoC_Stress-plots-20211008-154639
    │   │   └── plotter.py
    │   └── CtoC_Stress.csv
    ├── Ran1
    │   ├── Ran1-20211010-193613
    │   │   ├── Ran1log.csv
    │   │   └── Ran1-plots-20211010-193618
    │   ├── Ran1.csv
    │   └── Ran1terrain.csv
    ├── Terrain_Testing
    │   ├── Terrain_Testing20211010-044208
    │   │   ├── Terrain_Testinglog.csv
    │   │   └── Terrain_Testing-plots-20211010-044208
    │   ├── Terrain_Testing.csv
    │   └── Terrain_Testingterrain.csv
    └── Terrain_Testing2
        ├── Terrain_Testing220211010-050214
        │   ├── Terrain_Testing2log.csv
        │   └── Terrain_Testing2-plots-20211010-050214
        ├── Terrain_Testing220211010-050554
        │   ├── Terrain_Testing2log.csv
        │   └── Terrain_Testing2-plots-20211010-050554
        ├── Terrain_Testing220211010-050802
        │   ├── Terrain_Testing2log.csv
        │   └── Terrain_Testing2-plots-20211010-050802
        ├── Terrain_Testing220211010-192510
        │   ├── Terrain_Testing2log.csv
        │   └── Terrain_Testing2-plots-20211010-192510
        ├── Terrain_Testing220211010-192640
        │   ├── Terrain_Testing2log.csv
        │   └── Terrain_Testing2-plots-20211010-192640
        ├── Terrain_Testing2.csv
        └── Terrain_Testing2terrain.csv
```

44 directories, 4780 files

>[!NOTE] 
>Note that all the save logs have been exluded due to size issues with git. 