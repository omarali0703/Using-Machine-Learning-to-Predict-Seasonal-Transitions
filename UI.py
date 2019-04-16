import wx
# import Utils
import knn as knn
import linear_regression as l_r
import compare_model as c_m
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
import pandas as pd

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas


def get_choices():
    data_choices = os.listdir("./rawdata")
    choices = []
    for name in data_choices:
        if name.endswith(".csv"):
            choices.append(name)
    return choices


def beautify_title(title):
    title = title.replace('_raw_data.csv', '')
    return title.title()


print(beautify_title('test_raw_data.csv'))


class win(wx.Frame):
    figure=''
    def __init__(self, parent, title):

        super(win, self).__init__(parent, title=title, size=(1200, 900))

        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)
        button_size = wx.BoxSizer(wx.HORIZONTAL)
        header_size = wx.BoxSizer(wx.HORIZONTAL)
        footer_size = wx.BoxSizer(wx.HORIZONTAL)
        output_size = wx.BoxSizer(wx.VERTICAL)

        self.current_selection = ""
        self.btn = wx.Button(panel, 1, "Forcast KNN")
        self.l_btn = wx.Button(panel, 1, "Forcast Linear Regression")
        self.combine_btn = wx.Button(panel, 1, "Combine and Choose")

        self.lbl_choice = wx.StaticText(panel, -1, style=wx.ALIGN_CENTER)
        self.lbl_des = wx.StaticText(panel, -1, style=wx.ALIGN_LEFT)
        self.output_des = wx.StaticText(panel, -1, style=wx.ALIGN_LEFT)

        self.choice = wx.Choice(panel, choices=get_choices())

        self.figure = plt.figure()
        self.canvas = FigCanvas(panel, -1, self.figure)

        self.choice.Bind(wx.EVT_CHOICE, self.choice_event)
        self.btn.Bind(wx.EVT_BUTTON, self.on_clicked)
        self.l_btn.Bind(wx.EVT_BUTTON, self.on_clicked_l)
        self.combine_btn.Bind(wx.EVT_BUTTON, self.on_clicked_combo)

        self.lbl_choice.SetLabel('Data-set:')
        self.lbl_des.SetLabel(
            '\nFade in points -> The average temperature value for the given month'
            '\nActual Value -> The value calculated from the original dataset'
            '\nPredicted Value -> The value predicted from this chosen model'
            '\n'
            
            '\nFor KNN prediction'
            '\nEach box is representative of the average maximum and minimum temperature of its season from the last 10 years.'
            '\nThis allows for precise adaptaion over time whilst not allowing rapid changes to'
            '\naffect the results.'
            '\n'
            '\nFor combination selection'
            '\nThis method compares both methods with previous years and chooses the most accurate one'
            '\nto predict the next years data.'
        )

        header_size.Add(self.lbl_choice, wx.ALIGN_RIGHT, wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT, 10)
        header_size.Add(self.choice, wx.ALIGN_CENTER, wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT, 10)
        vbox.Add(header_size, 0, wx.ALIGN_CENTER, 5)

        vbox.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        button_size.Add(self.btn, wx.ALIGN_RIGHT, wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT, 5)
        button_size.Add(self.l_btn, wx.ALIGN_RIGHT, wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT, 5)
        button_size.Add(self.combine_btn, wx.ALIGN_RIGHT, wx.TOP|wx.BOTTOM|wx.LEFT|wx.RIGHT, 5)
        footer_size.Add(self.lbl_des, wx.ALIGN_RIGHT, wx.TOP|wx.BOTTOM|wx.LEFT, 10)

        output_size.Add(self.output_des, wx.ALIGN_RIGHT, wx.TOP|wx.BOTTOM|wx.LEFT, 10)
        footer_size.Add(output_size, wx.ALIGN_RIGHT, wx.TOP | wx.BOTTOM | wx.LEFT, 10)

        self.output_des.SetForegroundColour((0, 255, 0))
        vbox.Add(footer_size, 0, wx.ALIGN_LEFT, 5)
        vbox.Add(button_size, 0, wx.ALIGN_RIGHT, 5)
        panel.SetSizer(vbox)

        self.Centre()
        self.Show()
        self.Fit()

    def choice_event(self, event):
        self.current_selection = get_choices()[self.choice.GetSelection()]
        self.d = pd.read_csv('rawdata/' + self.current_selection)

    output_data = []

    def plot_linear_regression(self, year):
        ax = self.figure.add_subplot(111)
        ax.cla()
        ax.set_ylabel('Temperature (degress(c))')
        ax.set_xlabel('Season')
        ax.legend()
        ax.set_title('Prediction and Reflection for ' +beautify_title(self.current_selection) + ' ' + year + ' - Linear Regression')
        ax.set_facecolor((0, 0, 0))
        ax.set_ylim(bottom=-20)

        n_wi = l_r.plot(self.d, int(year), 'winter');
        n_sp = l_r.plot(self.d, int(year), 'spring');
        n_su = l_r.plot(self.d, int(year), 'summer');
        n_au = l_r.plot(self.d, int(year), 'autumn');

        n_data = [None, n_wi, None, None, n_sp, None, None, n_su, None, None, n_au, None]
        win.output_data = n_data

        f_data = [0, None, 2, 3, None, 5, 6, None, 8, 9, None, 11]

        for i in range(1, 12):
            if i not in [1, 4, 7, 10]:
                print(i)
                f_data[i] = (knn.get_max_temperature(self.d, i, int(year)))

        f_data[0] = knn.get_max_temperature(self.d, 12, int(year))

        ax.plot(['Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov'], n_data, 'rx')
        ax.plot(['Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov'], f_data, 'gx')

        y=int(year)

        sp_bar = knn.get_average_max(self.d, 10, y, 'spring')
        su_bar = knn.get_average_min(self.d, 10, y, 'summer')
        w_bar = knn.get_average_min(self.d, 10, y, 'winter')
        a_bar = knn.get_average_min(self.d, 10, y, 'autumn')

        sp_bar_low = knn.get_average_min(self.d, 10, y, 'spring')
        su_bar_low = knn.get_average_min(self.d, 10, y, 'summer')
        w_bar_low = knn.get_average_min(self.d, 10, y, 'winter')
        a_bar_low = knn.get_average_min(self.d, 10, y, 'autumn')

        print(sp_bar_low);
        ax.text(0, sp_bar + 0.01, "SPRING", fontsize=8)
        ax.text(0, su_bar + 0.01, "SUMMER", fontsize=8)
        ax.text(0, w_bar + 0.01, "WINTER", fontsize=8)
        ax.text(0, a_bar + 0.01, "AUTUMN", fontsize=8)

        ax.text(11, sp_bar_low + 0.01, "SPRING_LOW", fontsize=8)
        ax.text(11, su_bar_low + 0.01, "SUMMER_LOW", fontsize=8)
        ax.text(11, w_bar_low + 0.01, "WINTER_LOW", fontsize=8)
        ax.text(11, a_bar_low + 0.01, "AUTUMN_LOW", fontsize=8)

        alpha = 0.3
        rect_sp = patches.Rectangle((0, sp_bar_low), 12, sp_bar - sp_bar_low, linewidth=0, edgecolor='#ff00ff',facecolor='#ff00ff', alpha=alpha)
        rect_su = patches.Rectangle((0, su_bar_low), 12, su_bar - su_bar_low, linewidth=0, edgecolor='#00ffff',facecolor='#00ffff', alpha=alpha)
        rect_a = patches.Rectangle((0, a_bar_low), 12, a_bar - a_bar_low, linewidth=0, edgecolor='#ffffff00', facecolor='b', alpha=alpha)
        rect_w = patches.Rectangle((0, w_bar_low), 12, w_bar - w_bar_low, linewidth=0, edgecolor='#ffffff00', facecolor='#ffff00', alpha=alpha)

        ax.add_patch(rect_sp)
        ax.add_patch(rect_su)
        ax.add_patch(rect_a)
        ax.add_patch(rect_w)

        predict_patch = patches.Patch(color='red', label='Predicted Value')
        actual_patch = patches.Patch(color='blue', label='Actual Value')
        fade_patch = patches.Patch(color='yellow', label='Fade in/out Value')

        ax.legend(handles=[predict_patch, actual_patch, fade_patch])

        ax.axis([0, 11, 0, 30])
        self.output_des.SetLabel(win.display_results(year))

        self.canvas.draw()

    def plot(self, year):
        y = int(year)
        k = 5
        max_year = self.d.tail(1).iloc[0]['yyyy']

        if (max_year - y) < k // 2:
            knn.k_calc_type = "FORCAST METHOD"

            n_wi = knn.calculate_knn_forcast(self.d, k, y, "winter")
            n_sp = knn.calculate_knn_forcast(self.d, k, y, "spring")
            n_su = knn.calculate_knn_forcast(self.d, k, y, "summer")
            n_au = knn.calculate_knn_forcast(self.d, k, y, "autumn")
        else:
            knn.k_calc_type = "POINTCLOUD MID METHOD"

            n_wi = knn.calculate_knn_mid(self.d, k, y, "winter")
            n_sp = knn.calculate_knn_mid(self.d, k, y, "spring")
            n_su = knn.calculate_knn_mid(self.d, k, y, "summer")
            n_au = knn.calculate_knn_mid(self.d, k, y, "autumn")

        # using the actual data from the sheet. Nothing is generated, only plotted.
        o_data = [None, None, None, None, None, None, None, None, None, None, None, None]
        if y != (max_year + 1):
            o_wi = knn.construct_season_avg(self.d, y, "winter")
            o_sp = knn.construct_season_avg(self.d, y, "spring")
            o_su = knn.construct_season_avg(self.d, y, "summer")
            o_au = knn.construct_season_avg(self.d, y, "autumn")

            o_data = [None, o_wi, None, None, o_sp, None, None, o_su, None, None, o_au, None]

        f_data = [0, None, 2, 3, None, 5, 6, None, 8, 9, None, 11]

        for i in range(1, 12):
            if i not in [1, 4, 7, 10]:
                f_data[i] = (knn.get_max_temperature(self.d, i, y))

        f_data[0] = knn.get_max_temperature(self.d, 12, int(year))

        data = [None, n_wi, None, None, n_sp, None, None, n_su, None, None, n_au, None]
        win.output_data = data

        ax = self.figure.add_subplot(111)
        ax.cla()
        ax.set_ylabel('Temperature (degress(c))')

        ax.set_xlabel('Season')

        predict_patch = patches.Patch(color='red', label='Predicted Value')
        actual_patch = patches.Patch(color='blue', label='Actual Value')
        fade_patch = patches.Patch(color='yellow', label='Fade in/out Value')

        ax.legend(handles=[predict_patch, actual_patch, fade_patch])
        ax.set_title('Prediction and Reflection for ' + beautify_title(self.current_selection) + ' ' + str(year) + '{'+knn.k_calc_type+'}')

        #TODO fix prediction for 2019

        ax.set_facecolor((0, 0, 0))
        ax.set_ylim(bottom=-20)
        ax.axis([0, 11, 0, 30])

        ax.plot(['Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov'], data,'rx')
        ax.plot(['Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov'], o_data, 'bx')
        ax.plot(['Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov'], f_data, 'yx')

        sp_bar = knn.get_average_max(self.d, 10, y, 'spring')
        su_bar = knn.get_average_max(self.d, 10, y, 'summer')
        w_bar = knn.get_average_max(self.d, 10, y, 'winter')
        a_bar = knn.get_average_max(self.d, 10, y, 'autumn')

        sp_bar_low = knn.get_average_min(self.d, 10, y, 'spring')
        su_bar_low = knn.get_average_min(self.d, 10, y, 'summer')
        w_bar_low = knn.get_average_min(self.d, 10, y, 'winter')
        a_bar_low = knn.get_average_min(self.d, 10, y, 'autumn')

        ax.text(0, sp_bar+0.01, "SPRING", fontsize=8)
        ax.text(0, su_bar+0.01, "SUMMER", fontsize=8)
        ax.text(0, w_bar+0.01, "WINTER", fontsize=8)
        ax.text(0, a_bar+0.01, "AUTUMN", fontsize=8)

        ax.text(11, sp_bar_low+0.01, "SPRING_LOW", fontsize=8)
        ax.text(11, su_bar_low+0.01, "SUMMER_LOW", fontsize=8)
        ax.text(11, w_bar_low+0.01, "WINTER_LOW", fontsize=8)
        ax.text(11, a_bar_low+0.01, "AUTUMN_LOW", fontsize=8)


        alpha = 0.3

        rect_sp = patches.Rectangle((0, sp_bar_low), 12, sp_bar-sp_bar_low, linewidth=0, edgecolor='#ff00ff', facecolor='#ff00ff', alpha=alpha)
        rect_su = patches.Rectangle((0, su_bar_low), 12, su_bar-su_bar_low, linewidth=0, edgecolor='#00ffff', facecolor='#00ffff', alpha=alpha)
        rect_a = patches.Rectangle((0, a_bar_low), 12, a_bar-a_bar_low, linewidth=0, edgecolor='#ffffff00', facecolor='b', alpha=alpha)
        rect_w = patches.Rectangle((0, w_bar_low), 12, w_bar-w_bar_low, linewidth=0, edgecolor='#ffffff00', facecolor='#ffff00', alpha=alpha)

        ax.add_patch(rect_sp)
        ax.add_patch(rect_su)
        ax.add_patch(rect_a)
        ax.add_patch(rect_w)

        self.output_des.SetLabel(win.display_results(self, year))
        self.canvas.draw()

    def compare_model(self, year):
        result = c_m.produce_comparision(self.d, year)

        if result == 'lr':
            self.plot_linear_regression(year)
        elif result == 'knn':
            self.plot(year)

    def on_clicked(self, event):
        if self.current_selection != "":
            max_year = self.d.tail(1).iloc[0]['yyyy']

            check_date = wx.TextEntryDialog(None, 'enter date')
            check_date.ShowModal()
            date = check_date.GetValue()

            try:
                val = int(date)
                if int(date) > int(max_year):
                    check_selection = wx.MessageDialog(None, "Please enter a date before " + max_year + 1)
                    check_selection.ShowModal()
                else:
                    self.plot(val)

            except ValueError:
                check_selection = wx.MessageDialog(None, "Please enter a number")
                check_selection.ShowModal()
                return


        else:
            check_selection = wx.MessageDialog(None, "Please select a data-set")
            check_selection.ShowModal()
            return

        btn = event.GetEventObject().GetLabel()

    def on_clicked_l(self, event): #Linear reg button
        if self.current_selection != "":
            max_year = self.d.tail(1).iloc[0]['yyyy']
            check_date = wx.TextEntryDialog(None, 'enter date')
            check_date.ShowModal()
            date = check_date.GetValue()

            try:
                val = int(date)
                if int(date) >int(max_year):
                    check_selection = wx.MessageDialog(None, "Please enter a date before " + max_year + 1)
                    check_selection.ShowModal()
                else:
                    self.plot_linear_regression(val)

            except ValueError:
                check_selection = wx.MessageDialog(None, "Please enter a number")
                check_selection.ShowModal()
                return

        else:
            check_selection = wx.MessageDialog(None, "Please select a data-set")
            check_selection.ShowModal()
            return

    def on_clicked_combo(self, event):  # Combination button

        if self.current_selection != "":
            max_year = self.d.tail(1).iloc[0]['yyyy']
            check_date = wx.TextEntryDialog(None, 'enter date')
            check_date.ShowModal()
            date = check_date.GetValue()

            try:
                val = int(date)
                if int(date) > int(max_year):
                    check_selection = wx.MessageDialog(None, "Please enter a date before " + max_year + 1)
                    check_selection.ShowModal()
                else:
                    self.compare_model(val)

            except ValueError:
                check_selection = wx.MessageDialog(None, "Please enter a number")
                check_selection.ShowModal()
                return

            self.compare_model(date)

        else:
            check_selection = wx.MessageDialog(None, "Please select a data-set")
            check_selection.ShowModal()
            return

    def out(self, text):
        self.output_des.setLabel('Output: ' + text)

    def display_results(self, y):
        winter = win.output_data[1]
        spring = win.output_data[4]
        summer = win.output_data[7]
        autumn = win.output_data[10]

        output_text = ""

        sp_bar = knn.get_average_max(self.d, 10, y, 'spring')
        su_bar = knn.get_average_max(self.d, 10, y, 'summer')
        w_bar = knn.get_average_max(self.d, 10, y, 'winter')
        a_bar = knn.get_average_max(self.d, 10, y, 'autumn')

        sp_bar_low = knn.get_average_min(self.d, 10, y, 'spring')
        su_bar_low = knn.get_average_min(self.d, 10, y, 'summer')
        w_bar_low = knn.get_average_min(self.d, 10, y, 'winter')
        a_bar_low = knn.get_average_min(self.d, 10, y, 'autumn')


        if (winter > sp_bar_low and winter > w_bar) and spring < sp_bar:
            output_text += "There was no transition between WINTER and SPRING\n"
        if winter < w_bar and spring > sp_bar_low:
            output_text += "There was a transition between WINTER and SPRING\n"

        if (spring > su_bar_low and spring > sp_bar) and summer < su_bar:
            output_text += "There was no transition between SPRING and SUMMER\n"
        if spring < sp_bar and summer > sp_bar:
            output_text += "There was a transition between SPRING and SUMMER\n"

        if (summer > a_bar_low and summer > su_bar)and autumn < a_bar:
            output_text += "There was no transition between SUMMER and AUTUMN\n"
        if summer < su_bar and autumn < a_bar:
            output_text += "There was a transition between SUMMER and AUTUMN\n"

        if (autumn < w_bar and autumn > a_bar_low)and (winter < w_bar and winter> w_bar_low):
            output_text += "There was no transition between AUTUMN and WINTER\n"
        if (autumn < a_bar and winter < a_bar) or autumn < su_bar and autumn > a_bar:
            output_text += "There was a transition between AUTUMN and WINTER\n"
        # if autumn < su_bar_low and winter


        print(output_text)
        return output_text

app = wx.App()
win(None, 'Predicting Seasonal Transitions')
app.MainLoop()
