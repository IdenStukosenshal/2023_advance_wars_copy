Попытка реализовать свой вариант Advance wars (GBA) на Pygame(упрощённый wargame).

По символам из файла строится массив, по нему рисуется карта, строится взвешенный двунаправленный граф для вычисления пути.
Для каждого класса юнитов строится своя версия графа.
Рёбра к позиции юнитов в графе максимального веса, от позиции - указанные в карте
При передвижении рёбра восстанавливаются по карте.
Построение пути учитывает занятые ноды.





Управление:
* рамка перемещается стрелочками, 
* space поставить стартовую точку(перемещая рамку можно наблюдать построение пути и обход других юнитов)
* Ещё раз space - поставить конечную точку
* Backspace - отменить выделение

Requirements:
* Pygame
* Networkx
* algorithmx Для визуализации графа в браузере, не обязательно
    
    Примеры скриншотов Advance wars:

<img height="320" src="https://cdn.mobygames.com/screenshots/16327107-advance-wars-game-boy-advance-planes-flight-range.png" width="480"/>
<img height="320" src="https://cdn.mobygames.com/screenshots/16234224-advance-wars-game-boy-advance-terrain-information-screen-movemen.png" width="480"/>
