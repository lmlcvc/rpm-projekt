from gui import *
import matplotlib

matplotlib.use("TkAgg")


class SensorPage(tk.Frame):
    def update_data(self, files, values, measures):
        file_num = 0
        for file in files:
            figure = make_plots([file])
            canvas = FigureCanvasTkAgg(figure, self)
            canvas.draw()
            canvas.get_tk_widget().place(x=graph_coords[file_num][0], y=graph_coords[file_num][1])

            data = pd.read_csv(file, names=headers)
            average = str(round(data['Vrijednost'].mean(), 4))
            average_message = 'Prosječna vrijednost ' \
                              + values[file_num] + ': ' \
                              + average + measures[file_num]
            avg_label = tk.Label(self, text=average_message)
            avg_label.place(x=text_coords[file_num][0], y=text_coords[file_num][1])

            file_num += 1

    def init_label(self, sensor_label):
        label = tk.Label(self, text=sensor_label, font=LARGE_FONT)
        label.pack(pady=10, padx=10)

    def init_buttons(self, controller):
        button = tk.Button(self, text="Nazad", command=lambda: controller.show_frame(StartPage))
        button.place(x=50, y=20)

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)


class TMP116Page(SensorPage):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        TMP116Page.init_label(self, "TMP116")
        TMP116Page.init_buttons(self, controller)
        TMP116Page.update_data(self, [tmp116_csv], [temp_string], [temp_measurement])

        button_update = tk.Button(self, text="Ažuriraj", command=lambda: SensorPage.update_data(
            self, [tmp116_csv], [temp_string], [temp_measurement]
        ))
        button_update.place(x=100, y=20)

        value = pd.read_csv(tmp116_csv, names=headers).iloc[-1]['Vrijednost']
        indicator_label = tk.Label(self, text=construct_labels(temp=value, tips_wanted=True))
        indicator_label.place(x=100, y=650)


class HDC2010Page(SensorPage):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        HDC2010Page.init_label(self, "HDC2010")
        HDC2010Page.init_buttons(self, controller)
        HDC2010Page.update_data(self, [hdc2010_temp_csv, hdc2010_hum_csv],
                                [temp_string, hum_string], [temp_measurement, hum_measurement])

        button_update = tk.Button(self, text="Ažuriraj",
                                  command=lambda: SensorPage.update_data(self, [hdc2010_temp_csv, hdc2010_hum_csv],
                                                                         [temp_string, hum_string],
                                                                         [temp_measurement, hum_measurement]))
        button_update.place(x=100, y=20)

        value = pd.read_csv(hdc2010_temp_csv, names=headers).iloc[-1]['Vrijednost']
        indicator_label = tk.Label(self, text=construct_labels(temp=value, tips_wanted=True))
        indicator_label.place(x=100, y=650)

        value = pd.read_csv(hdc2010_hum_csv, names=headers).iloc[-1]['Vrijednost']
        indicator_label = tk.Label(self, text=construct_labels(humidity=value, tips_wanted=True))
        indicator_label.place(x=100, y=675)


class OPT3001Page(SensorPage):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        OPT3001Page.init_label(self, "OPT3001")
        OPT3001Page.init_buttons(self, controller)
        OPT3001Page.update_data(self, [opt3001_csv], [light_string], [light_measurement])

        button_update = tk.Button(self, text="Ažuriraj", command=lambda: SensorPage.update_data(
            self, [opt3001_csv], [light_string], [light_measurement]))
        button_update.place(x=100, y=20)

        value = pd.read_csv(opt3001_csv, names=headers).iloc[-1]['Vrijednost']
        indicator_label = tk.Label(self, text=construct_labels(light=value, tips_wanted=True))
        indicator_label.place(x=100, y=650)


class DPS301Page(SensorPage):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        DPS301Page.init_label(self, "DPS301")
        DPS301Page.init_buttons(self, controller)
        DPS301Page.update_data(self, [dps310_temp_csv, dps310_pressure_csv],
                               [temp_string, pressure_string], [temp_measurement, pressure_measurement])

        button_update = tk.Button(self, text="Ažuriraj",
                                  command=lambda: SensorPage.update_data(self, [dps310_temp_csv, dps310_pressure_csv],
                                                                         [temp_string, pressure_string],
                                                                         [temp_measurement, pressure_measurement]))
        button_update.place(x=100, y=20)

        value = pd.read_csv(dps310_temp_csv, names=headers).iloc[-1]['Vrijednost']
        indicator_label = tk.Label(self, text=construct_labels(temp=value, tips_wanted=True))
        indicator_label.place(x=100, y=650)

        value = pd.read_csv(dps310_pressure_csv, names=headers).iloc[-1]['Vrijednost']
        indicator_label = tk.Label(self, text=construct_labels(pressure=value, tips_wanted=True))
        indicator_label.place(x=100, y=675)


class StartPage(tk.Frame):

    # TODO: update grafova na početnoj strani
    # TODO: općenito - nazivi grafova, legende, boje

    def update_start_data(self):
        figure = make_plots([tmp116_csv, hdc2010_temp_csv, dps310_temp_csv], (3, 3))
        canvas = FigureCanvasTkAgg(figure, self)
        canvas.draw()
        canvas.get_tk_widget().place(x=100, y=250)

        figure = make_plots([hdc2010_hum_csv], (3, 3))
        canvas = FigureCanvasTkAgg(figure, self)
        canvas.draw()
        canvas.get_tk_widget().place(x=400, y=250)

        figure = make_plots([opt3001_csv], (3, 3))
        canvas = FigureCanvasTkAgg(figure, self)
        canvas.draw()
        canvas.get_tk_widget().place(x=700, y=250)

        figure = make_plots([dps310_pressure_csv], (3, 3))
        canvas = FigureCanvasTkAgg(figure, self)
        canvas.draw()
        canvas.get_tk_widget().place(x=1000, y=250)

        temp_value = round(np.average([pd.read_csv(tmp116_csv, names=headers)['Vrijednost'].iloc[-1],
                                       pd.read_csv(hdc2010_temp_csv, names=headers)['Vrijednost'].iloc[-1],
                                       pd.read_csv(dps310_temp_csv, names=headers)['Vrijednost'].iloc[-1]]), 4)
        hum_value = pd.read_csv(hdc2010_hum_csv, names=headers)['Vrijednost'].iloc[-1]
        light_value = pd.read_csv(opt3001_csv, names=headers)['Vrijednost'].iloc[-1]
        pressure_value = pd.read_csv(dps310_pressure_csv, names=headers)['Vrijednost'].iloc[-1]
        indicator_label = tk.Label(self, text=construct_labels(temp=temp_value, humidity=hum_value, light=light_value,
                                                               pressure=pressure_value, tips_wanted=True))
        indicator_label.place(x=100, y=675)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        StartPage.update_start_data(self)

        button_tmp = tk.Button(self, text="TMP116 očitanja", command=lambda: controller.show_frame(TMP116Page))
        button_tmp.pack()

        button_hdc = tk.Button(self, text="HDC2010 očitanja", command=lambda: controller.show_frame(HDC2010Page))
        button_hdc.pack()

        button_opt = tk.Button(self, text="OPT3001 očitanja", command=lambda: controller.show_frame(OPT3001Page))
        button_opt.pack()

        button_dps = tk.Button(self, text="DPS301 očitanja", command=lambda: controller.show_frame(DPS301Page))
        button_dps.pack()

        button_update = tk.Button(self, text="Ažuriraj", command=lambda: StartPage.update_start_data(self))
        button_update.place(x=100, y=20)
