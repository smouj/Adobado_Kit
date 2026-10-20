using System;
using System.Drawing;
using System.IO;
using System.IO.Compression;
using System.Net;
using System.Diagnostics;
using System.Threading;
using System.Windows.Forms;

class AppInfo {
    public string Name;
    public string Repo;
    public string Slug;
    public string Release;
    public string Exe;
    public string Url;
    public string AppDir;
    public Label Status;
    public Button OpenBtn;
    public Button InstallBtn;
}

class Launcher {
    static string baseDir;
    static AppInfo[] apps;
    static Form form;
    static string iconsDir;

    [STAThread]
    static void Main() {
        ServicePointManager.SecurityProtocol = (SecurityProtocolType)3072;
        baseDir = Directory.Exists("D:\\") ? "D:\\AdobadoApps" : Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "AdobadoApps");
        Directory.CreateDirectory(baseDir);
        iconsDir = Path.Combine(Application.StartupPath, "icons");

        apps = new AppInfo[] {
            NewApp("PhotoAdobado", "PhotoAdobado", "photo", "PhotoAdobado-windows-x64.zip"),
            NewApp("ArtAdobado", "ArtAdobado", "art", "ArtAdobado-windows-x64.zip"),
            NewApp("FilmAdobado", "FilmAdobado", "film", "FilmAdobado-windows-x64.zip"),
            NewApp("EffectAdobado", "EffectAdobado", "effect", "EffectAdobado-windows-x64.zip"),
            NewApp("LightAdobado", "LightAdobado", "light", "LightAdobado-windows-x64.zip"),
            NewApp("SoundAdobado", "SoundAdobado", "sound", "SoundAdobado-windows-x64.zip"),
            NewApp("DesignAdobado", "DesignAdobado", "design", "DesignAdobado-windows-x64.zip"),
            NewApp("PdfAdobado", "PdfAdobado", "pdf", "PdfAdobado-windows-x64.zip")
        };

        form = new Form();
        form.Text = "Adobado Kit Launcher";
        form.Size = new Size(1040, 820);
        form.StartPosition = FormStartPosition.CenterScreen;
        form.BackColor = Color.FromArgb(11, 14, 19);
        form.ForeColor = Color.FromArgb(238, 242, 246);
        form.Font = new Font("Segoe UI", 9f);
        try { form.Icon = new Icon(Path.Combine(Application.StartupPath, "launcher.ico")); } catch {}

        Label title = new Label();
        title.Text = "Adobado Kit";
        title.Font = new Font("Segoe UI", 24f, FontStyle.Bold);
        title.ForeColor = Color.FromArgb(238, 242, 246);
        title.AutoSize = true;
        title.Location = new Point(26, 18);
        form.Controls.Add(title);

        Label sub = new Label();
        sub.Text = "Herramientas creativas locales. Abre o instala cada app.";
        sub.Font = new Font("Segoe UI", 10f);
        sub.ForeColor = Color.FromArgb(152, 163, 177);
        sub.AutoSize = true;
        sub.Location = new Point(30, 64);
        form.Controls.Add(sub);

        FlowLayoutPanel flow = new FlowLayoutPanel();
        flow.Location = new Point(20, 96);
        flow.Size = new Size(990, 640);
        flow.AutoScroll = true;
        flow.BackColor = Color.FromArgb(11, 14, 19);
        form.Controls.Add(flow);

        foreach (AppInfo app in apps) {
            flow.Controls.Add(BuildCard(app));
        }

        Button folder = new Button();
        folder.Text = "Abrir carpeta de apps";
        folder.Location = new Point(30, 748);
        folder.Size = new Size(180, 32);
        folder.FlatStyle = FlatStyle.Flat;
        folder.FlatAppearance.BorderColor = Color.FromArgb(37, 44, 55);
        folder.BackColor = Color.FromArgb(18, 22, 29);
        folder.ForeColor = Color.FromArgb(238, 242, 246);
        folder.Click += delegate { Process.Start("explorer.exe", baseDir); };
        form.Controls.Add(folder);

        Button github = new Button();
        github.Text = "GitHub del Kit";
        github.Location = new Point(220, 748);
        github.Size = new Size(140, 32);
        github.FlatStyle = FlatStyle.Flat;
        github.FlatAppearance.BorderColor = Color.FromArgb(37, 44, 55);
        github.BackColor = Color.FromArgb(18, 22, 29);
        github.ForeColor = Color.FromArgb(238, 242, 246);
        github.Click += delegate { Process.Start("https://github.com/smouj/Adobado_Kit"); };
        form.Controls.Add(github);

        Application.Run(form);
    }

    static AppInfo NewApp(string name, string repo, string slug, string asset) {
        AppInfo a = new AppInfo();
        a.Name = name;
        a.Repo = repo;
        a.Slug = slug;
        a.Release = (name == "PhotoAdobado" || name == "FilmAdobado" || name == "SoundAdobado") ? "https://github.com/smouj/" + repo + "/releases/download/v0.1.0-alpha.1/" + asset : null;
        a.AppDir = Path.Combine(baseDir, name);
        a.Exe = Path.Combine(a.AppDir, name + ".exe");
        a.Url = "https://github.com/smouj/" + repo;
        return a;
    }

    static Panel BuildCard(AppInfo app) {
        Panel card = new Panel();
        card.Size = new Size(312, 190);
        card.BackColor = Color.FromArgb(18, 22, 29);
        card.BorderStyle = BorderStyle.FixedSingle;
        card.Margin = new Padding(8);

        PictureBox pic = new PictureBox();
        pic.Size = new Size(58, 58);
        pic.Location = new Point(14, 14);
        pic.SizeMode = PictureBoxSizeMode.Zoom;
        try { pic.Image = Image.FromFile(Path.Combine(iconsDir, app.Slug + ".png")); } catch { try { pic.Image = new Icon(Path.Combine(iconsDir, app.Slug + ".ico")).ToBitmap(); } catch {} }
        card.Controls.Add(pic);

        Label name = new Label();
        name.Text = app.Name;
        name.Font = new Font("Segoe UI", 12f, FontStyle.Bold);
        name.ForeColor = Color.FromArgb(238, 242, 246);
        name.AutoSize = true;
        name.Location = new Point(84, 16);
        card.Controls.Add(name);

        Label status = new Label();
        status.Font = new Font("Segoe UI", 8.5f);
        status.ForeColor = Color.FromArgb(152, 163, 177);
        status.AutoSize = true;
        status.Location = new Point(84, 42);
        card.Controls.Add(status);
        app.Status = status;

        Button open = new Button();
        open.Text = "Abrir";
        open.Location = new Point(14, 142);
        open.Size = new Size(132, 32);
        open.FlatStyle = FlatStyle.Flat;
        open.FlatAppearance.BorderColor = Color.FromArgb(37, 44, 55);
        open.BackColor = Color.FromArgb(23, 29, 39);
        open.ForeColor = Color.FromArgb(238, 242, 246);
        open.Click += delegate { OpenApp(app); };
        card.Controls.Add(open);
        app.OpenBtn = open;

        Button install = new Button();
        install.Location = new Point(156, 142);
        install.Size = new Size(142, 32);
        install.FlatStyle = FlatStyle.Flat;
        install.FlatAppearance.BorderColor = Color.FromArgb(37, 44, 55);
        install.BackColor = Color.FromArgb(23, 29, 39);
        install.ForeColor = Color.FromArgb(238, 242, 246);
        install.Click += delegate { if (app.Release == null) Process.Start(app.Url + "/releases"); else InstallApp(app); };
        card.Controls.Add(install);
        app.InstallBtn = install;

        LinkLabel link = new LinkLabel();
        link.Text = "Repo / releases";
        link.LinkColor = Color.FromArgb(108, 182, 255);
        link.ActiveLinkColor = Color.FromArgb(184, 243, 74);
        link.AutoSize = true;
        link.Location = new Point(14, 100);
        link.Click += delegate { Process.Start(app.Url + "/releases"); };
        card.Controls.Add(link);

        RefreshStatus(app);
        return card;
    }

    static void RefreshStatus(AppInfo app) {
        bool installed = File.Exists(app.Exe);
        if (app.Status != null) {
            app.Status.Text = installed ? "Instalada" : "No instalada";
            app.Status.ForeColor = installed ? Color.FromArgb(126, 231, 135) : Color.FromArgb(255, 159, 67);
        }
        if (app.InstallBtn != null) {
            if (app.Release == null) app.InstallBtn.Text = "Ver releases";
            else app.InstallBtn.Text = installed ? "Reinstalar" : "Instalar";
        }
    }

    static void OpenApp(AppInfo app) {
        if (!File.Exists(app.Exe)) {
            MessageBox.Show("La app no está instalada todavía. Usa Instalar.", "Adobado Kit", MessageBoxButtons.OK, MessageBoxIcon.Information);
            return;
        }
        try { Process.Start(app.Exe); } catch (Exception ex) { MessageBox.Show(ex.Message, "No se pudo abrir", MessageBoxButtons.OK, MessageBoxIcon.Error); }
    }

    static void InstallApp(AppInfo app) {
        if (File.Exists(app.Exe)) {
            DialogResult r = MessageBox.Show("¿Reinstalar " + app.Name + "?", "Adobado Kit", MessageBoxButtons.YesNo, MessageBoxIcon.Question);
            if (r != DialogResult.Yes) return;
        }
        string temp = Path.Combine(Path.GetTempPath(), "AdobadoKit_" + app.Slug);
        string zip = temp + ".zip";
        try {
            Cursor.Current = Cursors.WaitCursor;
            form.Text = "Adobado Kit Launcher - descargando " + app.Name + "...";
            WebClient wc = new WebClient();
            wc.Headers.Add("User-Agent", "AdobadoKitLauncher");
            wc.DownloadFile(app.Release, zip);
            if (Directory.Exists(temp)) Directory.Delete(temp, true);
            ZipFile.ExtractToDirectory(zip, temp);
            Directory.CreateDirectory(app.AppDir);
            CopyDir(temp, app.AppDir);
            string icon = Path.Combine(app.AppDir, app.Slug + ".ico");
            if (File.Exists(Path.Combine(iconsDir, app.Slug + ".ico"))) File.Copy(Path.Combine(iconsDir, app.Slug + ".ico"), icon, true);
            MakeShortcut(app, icon);
            RefreshStatus(app);
            form.Text = "Adobado Kit Launcher";
            MessageBox.Show(app.Name + " instalada. Acceso directo creado en el escritorio.", "Adobado Kit", MessageBoxButtons.OK, MessageBoxIcon.Information);
        } catch (Exception ex) {
            form.Text = "Adobado Kit Launcher";
            MessageBox.Show("No se pudo instalar: " + ex.Message + "\n\nPuedes descargarla manualmente desde el repo.", "Adobado Kit", MessageBoxButtons.OK, MessageBoxIcon.Error);
        } finally {
            Cursor.Current = Cursors.Default;
            try { if (File.Exists(zip)) File.Delete(zip); } catch {}
        }
    }

    static void CopyDir(string from, string to) {
        foreach (string f in Directory.GetFiles(from)) {
            File.Copy(f, Path.Combine(to, Path.GetFileName(f)), true);
        }
        foreach (string d in Directory.GetDirectories(from)) {
            string target = Path.Combine(to, Path.GetFileName(d));
            Directory.CreateDirectory(target);
            CopyDir(d, target);
        }
    }

    static void MakeShortcut(AppInfo app, string icon) {
        try {
            Type t = Type.GetTypeFromProgID("WScript.Shell");
            object shell = Activator.CreateInstance(t);
            string desktop = Environment.GetFolderPath(Environment.SpecialFolder.DesktopDirectory);
            object sc = t.InvokeMember("CreateShortcut", System.Reflection.BindingFlags.InvokeMethod, null, shell, new object[] { Path.Combine(desktop, app.Name + ".lnk") });
            Type st = sc.GetType();
            st.InvokeMember("TargetPath", System.Reflection.BindingFlags.SetProperty, null, sc, new object[] { app.Exe });
            st.InvokeMember("WorkingDirectory", System.Reflection.BindingFlags.SetProperty, null, sc, new object[] { app.AppDir });
            st.InvokeMember("IconLocation", System.Reflection.BindingFlags.SetProperty, null, sc, new object[] { icon + ",0" });
            st.InvokeMember("Description", System.Reflection.BindingFlags.SetProperty, null, sc, new object[] { app.Name + " - Adobado Kit" });
            st.InvokeMember("Save", System.Reflection.BindingFlags.InvokeMethod, null, sc, new object[] { });
        } catch {}
    }
}
