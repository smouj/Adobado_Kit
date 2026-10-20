using System;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.IO;
using System.IO.Compression;
using System.Net;
using System.Diagnostics;
using System.Threading;
using System.Windows.Forms;
using System.Reflection;

[assembly: AssemblyTitle("Adobado Kit Launcher")]
[assembly: AssemblyProduct("Adobado Kit")]
[assembly: AssemblyCompany("@smouj")]
[assembly: AssemblyDescription("Launcher for the Adobado creative apps")]
[assembly: AssemblyVersion("0.4.0.0")]
[assembly: AssemblyFileVersion("0.4.0.0")]
[assembly: AssemblyInformationalVersion("0.4.0")]

class AppInfo {
    public string Name;
    public string Repo;
    public string Slug;
    public string Release;
    public string Exe;
    public string Url;
    public string AppDir;
    public Color Accent;
    public Label Status;
    public Button OpenBtn;
    public Button InstallBtn;
}

class Launcher {
    const string OfficialAppIconFile = "Adobado-IconPack-Final-v1.ico";
    static string baseDir;
    static AppInfo[] apps;
    static Form form;
    static string iconsDir;
    static int cardWidth;
    static int cardHeight;
    static int columns;
    static bool compactCards;

    [STAThread]
    static void Main() {
        ServicePointManager.SecurityProtocol = (SecurityProtocolType)3072;
        baseDir = Directory.Exists("D:\\") ? "D:\\AdobadoApps" : Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "AdobadoApps");
        Directory.CreateDirectory(baseDir);
        iconsDir = Path.Combine(Application.StartupPath, "icons");

        apps = new AppInfo[] {
            NewApp("PhotoAdobado", "PhotoAdobado", "photo"),
            NewApp("ArtAdobado", "ArtAdobado", "art"),
            NewApp("FilmAdobado", "FilmAdobado", "film"),
            NewApp("EffectAdobado", "EffectAdobado", "effect"),
            NewApp("LightAdobado", "LightAdobado", "light"),
            NewApp("SoundAdobado", "SoundAdobado", "sound"),
            NewApp("DesignAdobado", "DesignAdobado", "design"),
            NewApp("PdfAdobado", "PdfAdobado", "pdf")
        };

        AnimatedBackground animatedForm = new AnimatedBackground();
        form = animatedForm;
        form.Text = "Adobado Kit Launcher";
        Rectangle workArea = Screen.FromPoint(Cursor.Position).WorkingArea;
        int windowWidth = Math.Min(1260, workArea.Width - 24);
        int windowHeight = Math.Min(920, workArea.Height - 24);
        form.Size = new Size(windowWidth, windowHeight);
        form.FormBorderStyle = FormBorderStyle.FixedSingle;
        form.MaximizeBox = false;
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
        sub.Text = "Herramientas para imagen, vídeo, ilustración, audio y documentos.";
        sub.Font = new Font("Segoe UI", 10f);
        sub.ForeColor = Color.FromArgb(152, 163, 177);
        sub.AutoSize = true;
        sub.Location = new Point(30, 64);
        form.Controls.Add(sub);

        PictureBox headerLogo = new PictureBox();
        headerLogo.Size = new Size(44, 44);
        headerLogo.Location = new Point(26, 14);
        headerLogo.SizeMode = PictureBoxSizeMode.Zoom;
        try { headerLogo.Image = Image.FromFile(Path.Combine(Application.StartupPath, "launcher.png")); } catch { try { headerLogo.Image = new Icon(Path.Combine(Application.StartupPath, "launcher.ico")).ToBitmap(); } catch {} }
        form.Controls.Add(headerLogo);
        title.Location = new Point(82, 18);

        AmbientSheen sheen = new AmbientSheen();
        sheen.Size = new Size(150, 86);
        sheen.Location = new Point(form.ClientSize.Width - 166, 4);
        sheen.Anchor = AnchorStyles.Top | AnchorStyles.Right;
        form.Controls.Add(sheen);

        int flowWidth = Math.Max(0, form.ClientSize.Width - 40);
        int flowHeight = Math.Max(0, form.ClientSize.Height - 96 - 58);
        int cardAreaWidth = Math.Max(0, flowWidth - 16);
        columns = cardAreaWidth >= 1120 ? 4 : (cardAreaWidth >= 760 ? 3 : 2);
        if (flowHeight < 430 && cardAreaWidth >= 600) columns = 4;
        int rows = (apps.Length + columns - 1) / columns;
        cardWidth = Math.Min(312, Math.Max(150, (cardAreaWidth - columns * 16) / columns));
        cardHeight = Math.Min(190, (flowHeight - rows * 16 - 20) / Math.Max(1, rows));
        if (cardHeight < 112 && cardAreaWidth >= 600) {
            columns = 4;
            rows = (apps.Length + columns - 1) / columns;
            cardWidth = Math.Min(312, Math.Max(150, (cardAreaWidth - columns * 16) / columns));
            cardHeight = Math.Min(170, (flowHeight - rows * 16 - 20) / Math.Max(1, rows));
        }
        cardHeight = Math.Max(112, cardHeight);
        compactCards = cardHeight < 176 || cardWidth < 230;

        FlowLayoutPanel flow = new FlowLayoutPanel();
        flow.Location = new Point(20, 96);
        flow.Size = new Size(flowWidth, flowHeight);
        flow.AutoScroll = false;
        flow.WrapContents = true;
        flow.BackColor = Color.Transparent;
        int unusedHeight = Math.Max(0, flowHeight - rows * (cardHeight + 16));
        int topSpace = Math.Max(4, unusedHeight / 2);
        flow.Padding = new Padding(4, topSpace, 4, Math.Max(4, unusedHeight - topSpace));
        form.Controls.Add(flow);

        foreach (AppInfo app in apps) {
            if (app.Name == "DesignAdobado" && columns == 3) {
                Panel spacer = new Panel();
                int tileWidth = cardWidth + 16;
                spacer.Size = new Size(Math.Max(8, tileWidth / 2 - 16), cardHeight);
                spacer.Margin = new Padding(8);
                spacer.BackColor = Color.Transparent;
                flow.Controls.Add(spacer);
            }
            flow.Controls.Add(BuildCard(app));
        }

        Button folder = new Button();
        folder.Text = "Abrir carpeta de apps";
        folder.Location = new Point(30, form.ClientSize.Height - 48);
        folder.Size = new Size(184, 36);
        StyleButton(folder, false);
        folder.Click += delegate { Process.Start("explorer.exe", baseDir); };
        form.Controls.Add(folder);

        Button github = new Button();
        github.Text = "Información del Kit";
        github.Location = new Point(224, form.ClientSize.Height - 48);
        github.Size = new Size(150, 36);
        StyleButton(github, false);
        github.Click += delegate { Process.Start("https://github.com/smouj/Adobado_Kit"); };
        form.Controls.Add(github);

        Label footer = new Label();
        footer.Text = "Tus archivos permanecen en tu equipo.";
        footer.Font = new Font("Segoe UI", 8.5f);
        footer.ForeColor = Color.FromArgb(137, 149, 164);
        footer.AutoSize = true;
        int footerWidth = TextRenderer.MeasureText(footer.Text, footer.Font).Width;
        footer.Location = new Point(form.ClientSize.Width - footerWidth - 30, form.ClientSize.Height - 31);
        footer.Anchor = AnchorStyles.Right | AnchorStyles.Bottom;
        form.Controls.Add(footer);

        Application.Run(form);
    }

    static AppInfo NewApp(string name, string repo, string slug) {
        AppInfo a = new AppInfo();
        a.Name = name;
        a.Repo = repo;
        a.Slug = slug;
        // Published alpha packages predate the current Adobado icons; don't offer an obsolete reinstall.
        a.Release = null;
        a.AppDir = Path.Combine(baseDir, name);
        a.Exe = Path.Combine(a.AppDir, name + ".exe");
        a.Url = "https://github.com/smouj/" + repo;
        a.Accent = AccentFor(slug);
        return a;
    }

    static Panel BuildCard(AppInfo app) {
        AppCard card = new AppCard(app.Accent);
        card.Size = new Size(cardWidth, cardHeight);
        card.Margin = new Padding(8);

        PictureBox pic = new PictureBox();
        pic.Size = new Size(compactCards ? 42 : 58, compactCards ? 42 : 58);
        pic.Location = new Point(compactCards ? 12 : 14, compactCards ? 12 : 14);
        pic.SizeMode = PictureBoxSizeMode.Zoom;
        try { pic.Image = Image.FromFile(Path.Combine(iconsDir, app.Slug + ".png")); } catch { try { pic.Image = new Icon(Path.Combine(iconsDir, app.Slug + ".ico")).ToBitmap(); } catch {} }
        card.Controls.Add(pic);

        Label name = new Label();
        name.Text = app.Name;
        name.Font = new Font("Segoe UI", compactCards ? 10.5f : 12f, FontStyle.Bold);
        name.ForeColor = Color.FromArgb(238, 242, 246);
        name.AutoSize = true;
        name.AutoEllipsis = true;
        name.MaximumSize = new Size(Math.Max(40, cardWidth - (compactCards ? 72 : 98)), 0);
        name.Location = new Point(compactCards ? 62 : 84, compactCards ? 13 : 16);
        card.Controls.Add(name);

        Label status = new Label();
        status.Font = new Font("Segoe UI", compactCards ? 7.5f : 8.5f);
        status.ForeColor = Color.FromArgb(152, 163, 177);
        status.AutoSize = true;
        status.Location = new Point(compactCards ? 62 : 84, compactCards ? 35 : 42);
        card.Controls.Add(status);
        app.Status = status;

        Button open = new Button();
        open.Text = "Abrir";
        int buttonY = cardHeight - (compactCards ? 38 : 48);
        int openWidth = compactCards ? Math.Max(52, (cardWidth - 32) / 2) : Math.Max(90, (cardWidth - 42) / 2);
        open.Location = new Point(compactCards ? 12 : 14, buttonY);
        open.Size = new Size(openWidth, compactCards ? 28 : 32);
        StyleButton(open, true);
        if (compactCards) open.Font = new Font("Segoe UI", 8f, FontStyle.Bold);
        open.Click += delegate { OpenApp(app); };
        card.Controls.Add(open);
        app.OpenBtn = open;

        Button install = new Button();
        int installX = open.Right + (compactCards ? 8 : 10);
        install.Location = new Point(installX, buttonY);
        install.Size = new Size(Math.Max(52, cardWidth - installX - (compactCards ? 12 : 14)), compactCards ? 28 : 32);
        StyleButton(install, false);
        if (compactCards) install.Font = new Font("Segoe UI", 7.5f);
        install.Click += delegate { if (app.Release == null) Process.Start(app.Url + "/releases"); else InstallApp(app); };
        card.Controls.Add(install);
        app.InstallBtn = install;

        LinkLabel link = new LinkLabel();
        link.Text = compactCards ? "Detalles" : "Ver funciones y detalles";
        link.LinkColor = Color.FromArgb(108, 182, 255);
        link.ActiveLinkColor = Color.FromArgb(184, 243, 74);
        link.Font = new Font("Segoe UI", compactCards ? 8f : 8.5f);
        link.LinkBehavior = LinkBehavior.HoverUnderline;
        link.AutoSize = true;
        link.Location = new Point(compactCards ? 62 : 84, compactCards ? 58 : 76);
        link.Click += delegate { Process.Start(app.Url); };
        card.Controls.Add(link);

        RefreshStatus(app);
        return card;
    }

    static void RefreshStatus(AppInfo app) {
        bool installed = File.Exists(app.Exe);
        if (app.Status != null) {
            app.Status.Text = installed ? "Instalada" : (compactCards ? "Sin instalar" : "No instalada");
            app.Status.ForeColor = installed ? Color.FromArgb(126, 231, 135) : Color.FromArgb(255, 159, 67);
        }
        if (app.InstallBtn != null) {
            if (app.Release == null) app.InstallBtn.Text = compactCards ? "Descargas" : "Ver descargas";
            else app.InstallBtn.Text = installed ? "Reinstalar" : "Instalar";
        }
    }

    static void OpenApp(AppInfo app) {
        if (!File.Exists(app.Exe)) {
            MessageBox.Show(compactCards ? "Todavía no está instalada. Abre «Descargas» para comprobar si hay una versión disponible." : "Todavía no está instalada. Abre «Ver descargas» para comprobar si hay una versión disponible.", "Adobado Kit", MessageBoxButtons.OK, MessageBoxIcon.Information);
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
            string icon = Path.Combine(app.AppDir, OfficialAppIconFile);
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
            object sc = t.InvokeMember("CreateShortcut", System.Reflection.BindingFlags.InvokeMethod, null, shell, new object[] { Path.Combine(desktop, app.Name + " App.lnk") });
            Type st = sc.GetType();
            st.InvokeMember("TargetPath", System.Reflection.BindingFlags.SetProperty, null, sc, new object[] { app.Exe });
            st.InvokeMember("WorkingDirectory", System.Reflection.BindingFlags.SetProperty, null, sc, new object[] { app.AppDir });
            st.InvokeMember("IconLocation", System.Reflection.BindingFlags.SetProperty, null, sc, new object[] { icon + ",0" });
            st.InvokeMember("Description", System.Reflection.BindingFlags.SetProperty, null, sc, new object[] { app.Name + " - Adobado Kit" });
            st.InvokeMember("Save", System.Reflection.BindingFlags.InvokeMethod, null, sc, new object[] { });
        } catch {}
    }

    static Color AccentFor(string slug) {
        switch (slug) {
            case "photo": return Color.FromArgb(255, 92, 92);
            case "art": return Color.FromArgb(232, 90, 200);
            case "film": return Color.FromArgb(255, 159, 67);
            case "effect": return Color.FromArgb(155, 123, 255);
            case "light": return Color.FromArgb(242, 201, 76);
            case "sound": return Color.FromArgb(53, 200, 216);
            case "design": return Color.FromArgb(123, 217, 87);
            default: return Color.FromArgb(79, 131, 232);
        }
    }

    static void StyleButton(Button button, bool primary) {
        button.FlatStyle = FlatStyle.Flat;
        button.FlatAppearance.BorderColor = primary ? Color.FromArgb(70, 99, 73) : Color.FromArgb(45, 54, 66);
        button.FlatAppearance.MouseOverBackColor = primary ? Color.FromArgb(32, 46, 39) : Color.FromArgb(29, 36, 47);
        button.FlatAppearance.MouseDownBackColor = Color.FromArgb(39, 47, 57);
        button.BackColor = primary ? Color.FromArgb(25, 36, 30) : Color.FromArgb(20, 25, 33);
        button.ForeColor = Color.FromArgb(238, 242, 246);
        button.Cursor = Cursors.Hand;
        button.Font = new Font("Segoe UI", 9f, primary ? FontStyle.Bold : FontStyle.Regular);
    }
}

sealed class AnimatedBackground : Form {
    Bitmap backgroundCache;
    static readonly Color[] Palette = new Color[] {
        Color.FromArgb(255, 92, 92), Color.FromArgb(232, 90, 200), Color.FromArgb(255, 159, 67),
        Color.FromArgb(155, 123, 255), Color.FromArgb(242, 201, 76), Color.FromArgb(53, 200, 216),
        Color.FromArgb(123, 217, 87), Color.FromArgb(79, 131, 232)
    };

    public AnimatedBackground() {
        SetStyle(ControlStyles.AllPaintingInWmPaint | ControlStyles.OptimizedDoubleBuffer, true);
    }

    internal Bitmap BackgroundImageCache { get { return backgroundCache; } }

    protected override void OnPaintBackground(PaintEventArgs e) {
        if (backgroundCache == null || backgroundCache.Width != ClientSize.Width || backgroundCache.Height != ClientSize.Height)
            RebuildBackground();
        if (backgroundCache != null) e.Graphics.DrawImageUnscaled(backgroundCache, 0, 0);
    }

    void RebuildBackground() {
        if (ClientSize.Width <= 0 || ClientSize.Height <= 0) return;
        Bitmap next = new Bitmap(ClientSize.Width, ClientSize.Height);
        Graphics g = Graphics.FromImage(next);
        try {
        g.SmoothingMode = SmoothingMode.AntiAlias;
        Rectangle bounds = ClientRectangle;
        using (LinearGradientBrush bg = new LinearGradientBrush(bounds, Color.FromArgb(14, 19, 28), Color.FromArgb(8, 11, 16), 35f))
            g.FillRectangle(bg, bounds);

        DrawGlow(g, new RectangleF(bounds.Width * 0.12f, bounds.Height * 0.05f, bounds.Width * 0.62f, bounds.Height * 0.58f), Palette[6], 22);
        DrawGlow(g, new RectangleF(bounds.Width * 0.55f, bounds.Height * 0.28f, bounds.Width * 0.56f, bounds.Height * 0.64f), Palette[3], 19);
        DrawGlow(g, new RectangleF(bounds.Width * 0.2f, bounds.Height * 0.55f, bounds.Width * 0.65f, bounds.Height * 0.5f), Palette[5], 12);
        } finally { g.Dispose(); }
        Bitmap previous = backgroundCache;
        backgroundCache = next;
        if (previous != null) previous.Dispose();
    }

    internal static void DrawGlow(Graphics g, RectangleF bounds, Color color, int alpha) {
        using (GraphicsPath path = new GraphicsPath()) {
            path.AddEllipse(bounds);
            using (PathGradientBrush glow = new PathGradientBrush(path)) {
                glow.CenterColor = Color.FromArgb(alpha, color);
                glow.SurroundColors = new Color[] { Color.FromArgb(0, color) };
                glow.FocusScales = new PointF(0.12f, 0.12f);
                g.FillPath(glow, path);
            }
        }
    }

    protected override void Dispose(bool disposing) {
        if (disposing) {
            if (backgroundCache != null) backgroundCache.Dispose();
        }
        base.Dispose(disposing);
    }
}

sealed class AmbientSheen : Control {
    readonly System.Windows.Forms.Timer timer;
    Bitmap[] frames;
    int currentFrame;
    static readonly Color[] Palette = new Color[] {
        Color.FromArgb(255, 92, 92), Color.FromArgb(232, 90, 200), Color.FromArgb(255, 159, 67),
        Color.FromArgb(155, 123, 255), Color.FromArgb(242, 201, 76), Color.FromArgb(53, 200, 216),
        Color.FromArgb(123, 217, 87), Color.FromArgb(79, 131, 232)
    };

    public AmbientSheen() {
        SetStyle(ControlStyles.UserPaint | ControlStyles.AllPaintingInWmPaint | ControlStyles.OptimizedDoubleBuffer, true);
        timer = new System.Windows.Forms.Timer();
        timer.Interval = 100;
        timer.Tick += delegate {
            if (frames != null && frames.Length > 0) {
                currentFrame = (currentFrame + 1) % frames.Length;
                Invalidate();
            }
        };
        timer.Start();
    }

    protected override void OnSizeChanged(EventArgs e) {
        base.OnSizeChanged(e);
        BuildFrames();
    }

    protected override void OnPaintBackground(PaintEventArgs e) {
        AnimatedBackground parent = Parent as AnimatedBackground;
        if (parent != null && parent.BackgroundImageCache != null)
            e.Graphics.DrawImage(
                parent.BackgroundImageCache,
                new Rectangle(0, 0, Width, Height),
                new Rectangle(Left, Top, Width, Height),
                GraphicsUnit.Pixel);
        else
            e.Graphics.Clear(Color.FromArgb(11, 14, 19));
    }

    void BuildFrames() {
        if (Width <= 0 || Height <= 0) return;
        Bitmap[] next = new Bitmap[24];
        for (int frame = 0; frame < next.Length; frame++) {
            Bitmap bitmap = new Bitmap(Width, Height, System.Drawing.Imaging.PixelFormat.Format32bppArgb);
            using (Graphics g = Graphics.FromImage(bitmap)) {
                g.Clear(Color.Transparent);
                g.SmoothingMode = SmoothingMode.AntiAlias;
                float phase = (float)(frame * Math.PI * 2.0 / next.Length);
                float span = (float)Math.Sin(phase) * Width * 0.10f;
                AnimatedBackground.DrawGlow(g, new RectangleF(Width * 0.10f + span, Height * 0.13f, Width * 0.52f, Height * 0.72f), Palette[6], 36);
                AnimatedBackground.DrawGlow(g, new RectangleF(Width * 0.42f - span, Height * 0.08f, Width * 0.55f, Height * 0.78f), Palette[5], 31);
                AnimatedBackground.DrawGlow(g, new RectangleF(Width * 0.30f + span * 0.55f, Height * 0.24f, Width * 0.48f, Height * 0.60f), Palette[3], 24);
            }
            next[frame] = bitmap;
        }
        Bitmap[] previous = frames;
        frames = next;
        currentFrame = 0;
        if (previous != null) foreach (Bitmap bitmap in previous) bitmap.Dispose();
    }

    protected override void OnPaint(PaintEventArgs e) {
        if (frames != null && frames.Length > currentFrame)
            e.Graphics.DrawImageUnscaled(frames[currentFrame], 0, 0);
    }

    protected override void Dispose(bool disposing) {
        if (disposing) {
            timer.Dispose();
            if (frames != null) foreach (Bitmap bitmap in frames) bitmap.Dispose();
        }
        base.Dispose(disposing);
    }
}

sealed class AppCard : Panel {
    readonly Color accent;
    bool hovered;

    public AppCard(Color accentColor) {
        accent = accentColor;
        SetStyle(ControlStyles.UserPaint | ControlStyles.AllPaintingInWmPaint | ControlStyles.OptimizedDoubleBuffer, true);
        BackColor = Color.FromArgb(17, 22, 30);
        MouseEnter += delegate { hovered = true; Invalidate(); };
        MouseLeave += delegate { hovered = false; Invalidate(); };
    }

    protected override void OnSizeChanged(EventArgs e) {
        base.OnSizeChanged(e);
        if (Width > 24 && Height > 24) {
            Region previous = Region;
            using (GraphicsPath path = RoundedRect(new Rectangle(0, 0, Width, Height), 12))
                Region = new Region(path);
            if (previous != null) previous.Dispose();
        }
    }

    protected override void OnPaint(PaintEventArgs e) {
        Graphics g = e.Graphics;
        g.SmoothingMode = SmoothingMode.AntiAlias;
        Rectangle r = new Rectangle(0, 0, Width - 1, Height - 1);
        using (GraphicsPath path = RoundedRect(r, 12)) {
            using (LinearGradientBrush fill = new LinearGradientBrush(r, Color.FromArgb(23, 29, 39), Color.FromArgb(15, 19, 27), 90f))
                g.FillPath(fill, path);
            using (Pen border = new Pen(hovered ? Color.FromArgb(122, accent) : Color.FromArgb(39, 48, 60), hovered ? 1.2f : 1f))
                g.DrawPath(border, path);
        }
        if (hovered) {
            Rectangle signature = new Rectangle(Width - 38, 1, 22, 2);
            using (GraphicsPath signaturePath = RoundedRect(signature, 1))
            using (SolidBrush brush = new SolidBrush(Color.FromArgb(150, accent)))
                g.FillPath(brush, signaturePath);
        }
        base.OnPaint(e);
    }

    protected override void OnControlAdded(ControlEventArgs e) {
        base.OnControlAdded(e);
        e.Control.MouseEnter += delegate { hovered = true; Invalidate(); };
        e.Control.MouseLeave += delegate { hovered = false; Invalidate(); };
    }

    static GraphicsPath RoundedRect(Rectangle r, int radius) {
        int d = radius * 2;
        GraphicsPath p = new GraphicsPath();
        p.AddArc(r.X, r.Y, d, d, 180, 90);
        p.AddArc(r.Right - d, r.Y, d, d, 270, 90);
        p.AddArc(r.Right - d, r.Bottom - d, d, d, 0, 90);
        p.AddArc(r.X, r.Bottom - d, d, d, 90, 90);
        p.CloseFigure();
        return p;
    }
}
