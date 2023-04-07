import matplotlib.pyplot as plt


def plot_routes(routes):
    # Считываем координаты точек из файла Data.txt
    with open(f'D:\Anatoly\Python\VKR_2_hard\data\Data.txt') as f:
        data = [line.split() for line in f.readlines()]

    # Создаем словарь, где ключами будут номера точек, а значениями - их координаты
    points = {int(d[0]): (float(d[1]), float(d[2])) for d in data}

    # Отображаем каждый маршрут на отдельном графике
    for i, route_points in enumerate(routes):
        # Получаем координаты точек маршрута из словаря
        route_coords = [points[p] for p in route_points]

        # Создаем график и добавляем точки маршрута
        fig, ax = plt.subplots()
        ax.plot([c[0] for c in route_coords], [c[1] for c in route_coords], 'o-')

        # Подписываем вершины номерами точек
        for j, coord in enumerate(route_coords):
            if route_points[j] == 0:
                label = 'Депо'
            else:
                label = str(route_points[j])
            ax.annotate(label, xy=coord, xytext=(5, 5), textcoords='offset points')
        ax.set_xlim(left=0)
        ax.set_ylim(bottom=0)
        # Добавляем заголовок и сохраняем график в файл
        ax.set_title(f'Маршрут {i+1}')
        plt.savefig(f'Route{i+1}.png')
        plt.show()
