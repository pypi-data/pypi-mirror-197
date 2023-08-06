import wx
import pandas as pd
from copy import deepcopy
from unidec.modules.isolated_packages.spreadsheet import *
from unidec.batch import UniDecBatchProcessor as BPEngine
from unidec.batch import *
from unidec.modules.html_writer import *
from unidec.GUniDec import UniDecApp


class HelpDlg(wx.Frame):
    def __init__(self, num=1, *args, **kw):
        super().__init__(*args, **kw)
        pathtofile = os.path.dirname(os.path.abspath(__file__))
        self.imagepath = os.path.join(pathtofile, "images")
        # print(pathtofile)
        # print(self.imagepath)
        if num == 1:
            self.help_frame()
        else:
            html = wx.html.HtmlWindow(self)
            html.SetPage("<html><body>You shouldn't see this!!! ERROR!!!!</body></html>")

    def help_frame(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, title="Help", size=(600, 600))
        html = wx.html.HtmlWindow(self)

        html_str = "<html><body>" \
                   "<h1>Overview</h1><p>" \
                   "Welcome to the UniDec Processing Pipeline (UPP)! " \
                   "This module is designed to help you process, deconvolve, " \
                   "and extract specific information from your data. " \
                   "Expanding on the batch processing features present in UniDec from the beginning, " \
                   "it is designed to interface with Excel/CSV files so that you can connect it with your workflows. " \
                   "</p>" \
                   "<h2>Basic Features</h2> <h3>Opening A File</h3><p>" \
                   "Although you can type everything directly into UPP, " \
                   "we recommend you start by importing your information from " \
                   "an Excel/CSV file. " \
                   "After you have your file ready, you can open it by clicking the" \
                   " \"File > Open File\" button and selecting your file. " \
                   "You can also open a file by dragging and dropping it onto the window. " \
                   "After opening the file, you should see it populate the main window like a spreadsheet.</p>" \
                   "<h3>What Do You Need In the Spreadsheet?</h3>" \
                   "<p>All you need is to specify the \"Sample name\" column with the file path. " \
                   "However, there are other optional parameters that you can specifiy. Note, capitalization is" \
                   " important, so make sure to specify caps carefully.</p>"

        html_str += array_to_html(basic_parameters, cols=["Parameter", "Required", "Description"], rows=None,
                                  colors=None, index=False, sortable=False)

        html_str += "<h3>Running UPP</h3><p>" \
                    "After you have opened your file, you can run UPP by clicking the \"Run\" button.</p> " \
                    "<p>There are two options to select to speed up the deconvolution and processing. " \
                    "The first is to use the already converted data. " \
                    "If you have already converted and averaged the data into a single spectrum," \
                    " you can select this option to skip the conversion step " \
                    "and speed up the program while you optimize the deconvolution.</p><p>" \
                    "The second option is to run the deconvolution engine. " \
                    "If you have already run the deconvolution engine on your data, " \
                    "you can select this option to skip the deconvolution step and speed up the program. " \
                    "This option is most useful if you have already deconvolved the data" \
                    " and want to adjust the peak matching or analysis.</p> "

        html_str += "<h3>Outputs</h3> <p>" \
                    "After running UPP, there are two key outputs. " \
                    "First, you will see one or more new tabs appear in the main window. " \
                    "These tabs will contain the results of the deconvolution and analysis. " \
                    "The results are saved to a \"results.xlsx\" file.</p> " \
                    "<p>Second, each deconvolution will generate an HTML reports that will be saved" \
                    " in the same directory as your data file in the _unidecfiles folder. " \
                    "You can open these reports in a web browser by clicking the \"Open All HTML Reports\" button. " \
                    "You can also open individual files by double clicking on individual cells.</p> "

        html_str += "<h3>Adjusting the Deconvolution Parameters</h3> <p>" \
                    "UPP will use the default UniDec parameters for deconvolution. " \
                    "However, you can adjust the deconvolution parameters " \
                    "by adding these optional rows in the spreadsheet: </p> "

        html_str += array_to_html(config_parameters, cols=["Parameter", "Required", "Description"], rows=None,
                                  colors=None, index=False, sortable=False)

        html_str += "<h2>Advanced Features</h2> <h3>Developing Workflows</h3><p>" \
                    "After you deconvolve your data, there are lots of things you can do with it. " \
                    "Because UPP is free and open-source, you can write in new functions and features " \
                    "that are customized for your workflow.</p> <p>For example, you could read in a column " \
                    "for \"Candidate Mass\" and search the peaks to if it is present. " \
                    "Take a look at the batch.py file on GitHub for ideas." \
                    "</p> <p>If you have new ideas for recipes, feel free to reach out for help. " \
                    "We are happy to help you develop your own recipes and workflows.</p> "

        html_str += "<h3>Workflow 1: Check Correct Masses or Pairings</h3><p>" \
                    "Here is an example recipe that checks if the correct pairing of massees" \
                    " and/or sequences is present. " \
                    "The column keyword of \"Sequence {n}\" defines a protein sequence " \
                    "were {n} is a number, such as \"Sequence 1\", or some other label. " \
                    "Each sequence cell should give the amino acid sequence of the " \
                    "protein chain or the mass of the species. </p> <p> " \
                    "Another key column is \"Correct{anything}\". UPP will look for a column with \"Correct\" in it. " \
                    "The \"Correct\" column should contain the correct pairing of the protein sequences. " \
                    "For example, if you have two protein sequences, \"Sequence 1\" and \"Sequence 2\", " \
                    "the \"Correct\" column should contain the pairing of the" \
                    " two sequences written as: \"Seq1+Seq2\". " \
                    "You can also other columns like \"Incorrect Homodimer\" as a column header " \
                    "with similar definitions (Seq2+Seq2 for example) " \
                    "and UPP will check if the incorrect pairing is present. " \
                    "You can also specify \"Ignored\" columns to ignore certain pairings. " \
                    "Note, you can also specify masses directly as correct, incorrect, or ignored. </p> <p> " \
                    "Finally, you can specify a Fixed or Variable Mod File to list potential sequence " \
                    "modifications (see more info below) and a \"Tolerance\" to specify the peak matching tolerance. " \
                    "Using all this information, the workflow will then search for the correct" \
                    " and incorrectly paired masses in the deconvolution results (with any possible modifications). " \
                    "If the correct mass/pairing is present, it will color the peak green. " \
                    "If the incorrect mass/pairing is present, it will color the peak red. " \
                    "If an ignored mass/pairng is present, it will color the peak blue. " \
                    "If no mathes are found for a given peak (unknown), it will color the peak yellow. </p> <p> " \
                    "The final results spreadsheet will contain the percentage of the signal " \
                    "that is correct, incorrect, ignored, and unknown." \
                    "It will also give the percentage of correct and incorrect " \
                    "after ignoring the unknown and ignored. " \
                    "Additional details on keywords are provided below. "

        html_str += array_to_html(recipe_w, cols=["Parameter", "Required", "Description"], rows=None,
                                  colors=None, index=False, sortable=False)

        html_str += "</body></html>"

        html.SetPage(html_str)


class MyFileDropTarget(wx.FileDropTarget):
    """"""

    def __init__(self, window):
        """Constructor"""
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, filenames):
        """
        When files are dropped, either open a single file or run in batch.
        """
        path = filenames[0]
        self.window.load_file(path)
        return 0


class UPPApp(wx.Frame):
    """"""

    def __init__(self, nrows=2, ncolumns=2, title="UniDec Processing Pipeline"):
        """Constructor"""
        wx.Frame.__init__(self, parent=None, title=title, size=(1800, 600))
        self.use_decon = True
        self.use_converted = True
        self.use_interactive = False
        self.bpeng = BPEngine()

        menu = wx.Menu()
        # Open File Menu
        open_file_menu_item = menu.Append(wx.ID_ANY, "Open File", "Open a CSV or Excel file")
        self.Bind(wx.EVT_MENU, self.on_load_file, open_file_menu_item)
        menu.AppendSeparator()

        # Save File Menu
        save_file_menu_item = menu.Append(wx.ID_ANY, "Save File", "Save a CSV or Excel file")
        self.Bind(wx.EVT_MENU, self.on_save_file, save_file_menu_item)
        menu.AppendSeparator()

        # Add Files Menu
        add_files_menu_item = menu.Append(wx.ID_ANY, "Add Data Files", "Add Data Files")
        self.Bind(wx.EVT_MENU, self.on_add_files, add_files_menu_item)

        # Clear everything on the panel
        clear_everything_menu_item = menu.Append(wx.ID_ANY, "Clear All", "Clear Everything")
        self.Bind(wx.EVT_MENU, self.clear_all, clear_everything_menu_item)

        help_menu = wx.Menu()
        # Open File Menu
        help_manu_item = help_menu.Append(wx.ID_ANY, "Help Me!", "Open a help page")
        self.Bind(wx.EVT_MENU, self.on_help_page, help_manu_item)

        # Create the menubar
        menuBar = wx.MenuBar()
        menuBar.Append(menu, "&File")
        menuBar.Append(help_menu, "&Help")
        self.SetMenuBar(menuBar)

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)

        # Insert a button and bind it with a handler called on_run
        self.runbtn = wx.Button(panel, label="Run All")
        self.runbtn.Bind(wx.EVT_BUTTON, self.on_run)
        hsizer.Add(self.runbtn, 0)

        # Insert a button and bind it with a handler called on_run
        self.runbtn2 = wx.Button(panel, label="Run Selected")
        self.runbtn2.Bind(wx.EVT_BUTTON, self.on_run_selected)
        hsizer.Add(self.runbtn2, 0)

        # Insert Spacer Text
        hsizer.Add(wx.StaticText(panel, label="   "), 0)

        # Insert a button for Open All HTML Reports and bind to function
        btn = wx.Button(panel, label="Open All HTML Reports")
        btn.Bind(wx.EVT_BUTTON, self.on_open_all_html)
        hsizer.Add(btn, 0)

        # Insert a button for Run in UniDec and bind to function
        btn = wx.Button(panel, label="Open in UniDec")
        btn.Bind(wx.EVT_BUTTON, self.on_open_unidec)
        hsizer.Add(btn, 0)

        # Insert a static text of directory
        # hsizer.Add(wx.StaticText(panel, label="   Data Directory:", style=wx.ALIGN_CENTER_VERTICAL))
        # Insert a text box to read out the directory
        # self.dirtxtbox = wx.TextCtrl(panel, size=(400, -1))
        # hsizer.Add(self.dirtxtbox, 0, wx.EXPAND)
        # Add a button to set the directory
        # btn = wx.Button(panel, label="...")

        # Insert a static text of tolerance
        # hsizer.Add(wx.StaticText(panel, label="   Tolerance:", style=wx.ALIGN_CENTER_VERTICAL))
        # Insert a text box to read out the directory
        # self.tolbox = wx.TextCtrl(panel, size=(50, -1))
        # self.tolbox.SetValue("50")
        # hsizer.Add(self.tolbox, 0, wx.EXPAND)
        # hsizer.Add(wx.StaticText(panel, label="Da   ", style=wx.ALIGN_CENTER_VERTICAL))

        # Insert Spacer Text
        hsizer.Add(wx.StaticText(panel, label="   "), 0)

        # Insert a checkbox to select whether to use already converted data
        self.useconvbox = wx.CheckBox(panel, label="Use Converted Data  ")
        hsizer.Add(self.useconvbox, 0, wx.EXPAND)
        self.useconvbox.SetValue(self.use_converted)

        # Insert a checkbox to select whether to use already deconvolved data
        self.usedeconbox = wx.CheckBox(panel, label="Deconvolve Data  ")
        hsizer.Add(self.usedeconbox, 0, wx.EXPAND)
        self.usedeconbox.SetValue(self.use_decon)

        # Insert a checkbox to select whether to generate interactive HTML reports
        self.interactivebox = wx.CheckBox(panel, label="Interactive Reports  ")
        hsizer.Add(self.interactivebox, 0, wx.EXPAND)
        self.interactivebox.SetValue(self.use_interactive)

        # Insert Spacer Text
        hsizer.Add(wx.StaticText(panel, label="   "), 0)

        # Insert a button to hide columns
        self.hidebtn = wx.Button(panel, label="Hide Columns")
        self.hidebtn.Bind(wx.EVT_BUTTON, self.on_hide_columns)
        hsizer.Add(self.hidebtn, 0)
        self.hide_col_flag = False

        # Insert a button to hide columns with height in the title
        self.hideheightbtn = wx.Button(panel, label="Hide Height Columns")
        self.hideheightbtn.Bind(wx.EVT_BUTTON, self.on_hide_height_columns)
        hsizer.Add(self.hideheightbtn, 0)
        self.hide_height_flag = False

        # Insert a button to hide columns with % in the title
        self.hidepercentbtn = wx.Button(panel, label="Hide % Columns")
        self.hidepercentbtn.Bind(wx.EVT_BUTTON, self.on_hide_percent_columns)
        hsizer.Add(self.hidepercentbtn, 0)
        self.hide_percentcol_flag = False

        # Insert Spacer Text
        hsizer.Add(wx.StaticText(panel, label="   "), 0)

        # Insert a button to hide columns that are empty
        self.hideemptybtn = wx.Button(panel, label="Hide Empty Columns")
        self.hideemptybtn.Bind(wx.EVT_BUTTON, self.on_hide_empty_columns)
        hsizer.Add(self.hideemptybtn, 0)

        sizer.Add(hsizer, 0, wx.ALL | wx.EXPAND)

        self.ss = SpreadsheetPanel(self, panel, nrows, ncolumns).ss
        self.ss.set_col_headers(["Sample name", "Data Directory"])
        sizer.Add(self.ss, 1, wx.EXPAND)

        file_drop_target = MyFileDropTarget(self)
        self.ss.SetDropTarget(file_drop_target)

        panel.SetSizer(sizer)
        self.Show()

    def on_run(self, event=None):
        print("Run button pressed")
        self.runbtn.SetBackgroundColour("red")
        self.get_from_gui()
        self.bpeng.run_df(decon=self.use_decon, use_converted=self.use_converted, interactive=self.use_interactive)
        self.ss.set_df(self.bpeng.rundf)
        self.runbtn.SetBackgroundColour("green")
        if not self.hide_col_flag:
            self.on_hide_columns()

    def on_run_selected(self, event=None, rows=None):
        self.runbtn2.SetBackgroundColour("red")
        if rows is None:
            # Get Selected Rows
            selected_rows = list(self.ss.get_selected_rows())
        else:
            selected_rows = rows
        print("Running Selected Rows:", selected_rows)
        # Get Sub Dataframe with Selected Rows
        self.get_from_gui()
        topdf = deepcopy(self.bpeng.rundf)
        subdf = self.bpeng.rundf.iloc[selected_rows]
        # Run SubDF
        subdf2 = self.bpeng.run_df(df=subdf, decon=self.use_decon, use_converted=self.use_converted,
                                   interactive=self.use_interactive)
        # Update the main dataframe
        # topdf.iloc[selected_rows] = subdf2
        topdf = set_row_merge(topdf, subdf, selected_rows)
        self.bpeng.rundf = topdf
        self.ss.set_df(self.bpeng.rundf)
        # Finish by coloring the button green
        self.runbtn2.SetBackgroundColour("green")
        if not self.hide_col_flag:
            self.on_hide_columns()

    def clear_all(self, event=None):
        self.ss.delete_all()
        self.ss.set_col_headers(["Sample name", "Data Directory"])

    def load_file(self, filename):
        print("Loading File:", filename)
        try:
            self.ss.delete_all()
        except Exception:
            pass
        self.bpeng.top_dir = os.path.dirname(filename)
        df = file_to_df(filename)
        self.ss.set_df(df)
        # dirname = os.path.dirname(filename)
        # self.set_dir_tet_box(dirname)
        self.reset_hidden_columns()

    def on_load_file(self, event):
        print("Load button pressed")
        # Create a file dialog
        with wx.FileDialog(self, "Open CSV or Excel File",
                           wildcard="CSV or Excel files (*.csv; *.xlsx; *.xls)|*.csv; *.xlsx; *.xls|"
                                    "CSV files (*.csv)|*.csv|"
                                    "Excel files (*.xlsx; *.xls)|*.xlsx; *.xls",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            # Show the dialog and retrieve the user response. If it is the OK response,
            # process the data.
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            self.load_file(pathname)

    def on_save_file(self, event):
        print("Save button pressed")
        # Create a file dialog
        with wx.FileDialog(self, "Save CSV or Excel File",
                           wildcard="CSV or Excel files (*.csv; *.xlsx; *.xls)|*.csv; *.xlsx; *.xls|"
                                    "CSV files (*.csv)|*.csv|"
                                    "Excel files (*.xlsx; *.xls)|*.xlsx; *.xls",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            # Show the dialog and retrieve the user response. If it is the OK response,
            # process the data.
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            self.ss.save_file(pathname)

    # def set_dir_tet_box(self, dirname):
    #    self.dirtxtbox.SetValue(dirname)

    def get_from_gui(self):
        self.use_converted = self.useconvbox.GetValue()
        self.use_decon = self.usedeconbox.GetValue()
        self.use_interactive = self.interactivebox.GetValue()

        # dirname = self.dirtxtbox.GetValue()
        # tol = self.tolbox.GetValue()
        # self.bpeng.data_dir = dirname
        # try:
        #    self.bpeng.tolerance = float(tol)
        # except Exception as e:
        #    print("Error with Tolerance Value. Using default value of 50 Da", e)
        #    self.bpeng.tolerance = 10
        #    self.tolbox.SetValue("10")

        self.ss.remove_empty()
        ssdf = self.ss.get_df()
        self.bpeng.rundf = ssdf

    def on_open_all_html(self, event):
        print("Open All HTML Reports button pressed")
        self.bpeng.open_all_html()

    def on_open_unidec(self, event):
        ssdf = self.ss.get_df()
        self.bpeng.rundf = ssdf
        selected_rows = list(self.ss.get_selected_rows())
        print(selected_rows)
        row = self.bpeng.rundf.iloc[selected_rows[0]]
        self.open_unidec(row)

    def open_unidec(self, row):
        print("Opening in UniDec:", row)
        filepath = self.bpeng.get_file_path(row)
        if filepath is not None:
            print("Launching UniDec:")
            app = UniDecApp(path=filepath)
            app.eng.unidec_imports(efficiency=False)
            app.after_unidec_run()
            app.on_pick_peaks()
            if self.bpeng.correct_pair_mode:
                self.bpeng.run_correct_pair(row, app.eng.pks)
                app.after_pick_peaks()
            app.start()

    def on_add_files(self, event=None):

        wildcard = "CSV or Excel files (*.csv; *.xlsx; *.xls)|*.csv; *.xlsx; *.xls|CSV files (*.csv)|*.csv|Excel files (*.xlsx; *.xls)|*.xlsx; *.xls"
        wildcard = "Any files (*.*) |*.*| " \
                   "Known file types (*.raw; *.d; *.mzML; *.mzXML; *.txt; *.csv; *.dat; *.npz)|" \
                   "*.raw; *.d; *.mzML; *.mzXML; *.txt; *.csv; *.dat; *.npz|" \
                   "Thermo RAW files (*.raw)|*.raw|" \
                   "Agilent D files (*.d)|*.d|" \
                   "mzML files (*.mzML)|*.mzML|" \
                   "mzXML files (*.mzXML)|*.mzXML|" \
                   "Text files (*.txt)|*.txt|" \
                   "CSV files (*.csv)|*.csv|" \
                   "Dat files (*.dat)|*.dat|" \
                   "NPZ files (*.npz)|*.npz"

        # Create a file selection dialog
        with wx.FileDialog(self, "Select Files to Add",
                           wildcard=wildcard,
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE) as fileDialog:
            # Show the dialog and retrieve the user response. If it is the OK response,
            # process the data.

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            # Proceed loading the file chosen by the user
            paths = fileDialog.GetPaths()
            self.add_files(paths)

    def add_files(self, paths):
        print("Adding Files:", paths)
        self.get_from_gui()
        # Add paths list to the datafram in the "Sample name" column
        sample_names = [os.path.basename(path) for path in paths]
        data_dir = [os.path.dirname(path) for path in paths]
        newdf = pd.DataFrame({"Sample name": sample_names, "Data Directory": data_dir})
        self.bpeng.rundf = pd.concat([self.bpeng.rundf, newdf], ignore_index=True)

        self.ss.set_df(self.bpeng.rundf)
        self.reset_hidden_columns()

    def on_hide_columns(self, event=None, reset=False):
        columns_to_hide = ["Tolerance", "File", "Time", "Config", "Sequence", "Directory", "Matches"]
        if not self.hide_col_flag and not reset:
            for keyword in columns_to_hide:
                self.ss.hide_columns_by_keyword(keyword)
            self.hide_col_flag = True
            self.hidebtn.SetLabel("Show Columns")
        else:
            self.hidebtn.SetLabel("Hide Columns")
            self.ss.show_all_columns()
            self.hide_col_flag = False

    def reset_hidden_columns(self):
        self.on_hide_columns(reset=True)
        self.on_hide_height_columns(reset=True)
        self.on_hide_percent_columns(reset=True)

    def on_hide_empty_columns(self, event=None):
        self.ss.hide_empty_columns()

    def on_hide_height_columns(self, event=None, reset=False):
        if not self.hide_height_flag and not reset:
            self.ss.hide_columns_by_keyword("Height")
            self.hide_height_flag = True
            self.hideheightbtn.SetLabel("Show Height Columns")
        else:
            self.hideheightbtn.SetLabel("Hide Height Columns")
            self.ss.show_columns_by_keyword("Height")
            self.hide_height_flag = False

    def on_hide_percent_columns(self, event=None, reset=False):
        if not self.hide_percentcol_flag and not reset:
            self.ss.hide_columns_by_keyword("%")
            self.hide_percentcol_flag = True
            self.hidepercentbtn.SetLabel("Show % Columns")
        else:
            self.hidepercentbtn.SetLabel("Hide % Columns")
            self.ss.show_columns_by_keyword("%")
            self.hide_percentcol_flag = False

    def on_help_page(self, event=None):
        print("Help button pressed")
        dlg = HelpDlg()
        dlg.Show()

    def on_exit(self, event=None):
        self.Close()


if __name__ == "__main__":
    app = wx.App()
    frame = UPPApp()
    frame.usedeconbox.SetValue(True)
    path = "C:\\Data\\Wilson_Genentech\\sequences_short.xlsx"
    path = "C:\\Data\\Wilson_Genentech\\BsAb\\BsAb test short.xlsx"

    # frame.on_help_page()
    # exit()
    if False:
        frame.load_file(path)
        # frame.set_dir_tet_box("C:\\Data\\Wilson_Genentech\\Data")
        # print(df)
        # frame.on_run()
        # frame.on_run_selected(rows=[1])
        # frame.on_run_selected(rows=[0])
        # frame.on_add_files()

    app.MainLoop()
