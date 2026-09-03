import sys
import os
import json
import shutil
import ctypes
from ctypes import wintypes
from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QDialog, 
                             QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, 
                             QFrame, QComboBox, QSlider, QCheckBox,
                             QFileDialog, QGridLayout)
from PySide6.QtCore import Qt, QTimer, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QKeySequence, QIcon, QPixmap, QPainterPath

PALETTES = {
    "Rosa": {"bg": "#FFE4E1", "arc": "#FF69B4", "text": "#FF1493", "btn": "#FFB6C1", "hover": "#FFC0CB"},
    "Lila": {"bg": "#F3E5F5", "arc": "#BA68C8", "text": "#8E24AA", "btn": "#CE93D8", "hover": "#E1BEE7"},
    "Menta": {"bg": "#E8F5E9", "arc": "#81C784", "text": "#388E3C", "btn": "#A5D6A7", "hover": "#C8E6C9"},
    "Melocotón": {"bg": "#FFF3E0", "arc": "#FFB74D", "text": "#F57C00", "btn": "#FFCC80", "hover": "#FFE0B2"},
    "Cielo": {"bg": "#E0F7FA", "arc": "#4DD0E1", "text": "#00838F", "btn": "#81D4FA", "hover": "#B3E5FC"},
    "Sol": {"bg": "#FFFDE7", "arc": "#FFF176", "text": "#FBC02D", "btn": "#FFF59D", "hover": "#FFF9C4"},
    "Tierra": {"bg": "#EFEBE9", "arc": "#A1887F", "text": "#5D4037", "btn": "#BCAAA4", "hover": "#D7CCC8"},
    "Lavanda": {"bg": "#E1F5FE", "arc": "#9575CD", "text": "#512DA8", "btn": "#B39DDB", "hover": "#D1C4E9"},
    "Cereza": {"bg": "#FFEBEE", "arc": "#EF5350", "text": "#C62828", "btn": "#EF9A9A", "hover": "#FFCDD2"}
}

APP_NAME = "CuteTimer"
DOCUMENTS_DIR = os.path.join(os.path.expanduser("~"), "Documents", APP_NAME)

if not os.path.exists(DOCUMENTS_DIR):
    try:
        os.makedirs(DOCUMENTS_DIR)
    except Exception:
        pass

CONFIG_FILE = os.path.join(DOCUMENTS_DIR, "config.json")
ASSETS_DIR = os.path.join(DOCUMENTS_DIR, "timer_assets")

class ConfigDialog(QDialog):
    def __init__(self, current_seconds, current_opacity, current_palette, current_fontsize, show_hours, show_minutes, bg_image, current_thickness, current_appsize, current_flags, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(400, 580)
        
        self.bg_image = bg_image

        self.frame = QFrame(self)
        self.frame.setGeometry(0, 0, 400, 580)
        self.frame.setStyleSheet("""
            QFrame { background-color: #2b2b2b; border-radius: 12px; border: 2px solid #565b5e; }
            QLabel { color: #dce4ee; font-family: 'Segoe UI', Arial; font-size: 12px; font-weight: bold; border: none; }
            QSpinBox, QComboBox { background-color: #343638; color: #dce4ee; border: 1px solid #565b5e; border-radius: 6px; padding: 4px; font-size: 12px; }
            QSpinBox::up-button, QSpinBox::down-button { background-color: #565b5e; width: 14px; }
            QSlider::groove:horizontal { border-radius: 4px; height: 6px; background: #343638; }
            QSlider::handle:horizontal { background: #1f6aa5; width: 14px; margin: -4px 0; border-radius: 7px; }
            QPushButton { background-color: #1f6aa5; color: #dce4ee; border-radius: 6px; padding: 6px; font-family: 'Segoe UI', Arial; font-weight: bold; border: none; }
            QPushButton:hover { background-color: #144870; }
            QPushButton#btn_cancel { background-color: #343638; border: 1px solid #565b5e; }
            QPushButton#btn_cancel:hover { background-color: #565b5e; }
            QCheckBox { color: #dce4ee; font-family: 'Segoe UI', Arial; font-weight: bold; font-size: 12px; spacing: 5px; border: none; }
            QCheckBox::indicator { width: 14px; height: 14px; border-radius: 4px; border: 1px solid #565b5e; background-color: #343638; }
            QCheckBox::indicator:checked { background-color: #1f6aa5; border-color: #1f6aa5; } 
        """)
        
        layout = QVBoxLayout(self.frame)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        title_label = QLabel("⚙️ Configuración Sistema Unificado")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        h_layout = QHBoxLayout()
        self.h_spin = QSpinBox(); self.h_spin.setRange(0, 99)
        self.m_spin = QSpinBox(); self.m_spin.setRange(0, 59)
        self.s_spin = QSpinBox(); self.s_spin.setRange(0, 59)
        
        h, rem = divmod(current_seconds, 3600)
        m, s = divmod(rem, 60)
        self.h_spin.setValue(h)
        self.m_spin.setValue(m)
        self.s_spin.setValue(s)
        
        for widget in [QLabel("H:"), self.h_spin, QLabel("M:"), self.m_spin, QLabel("S:"), self.s_spin]:
            h_layout.addWidget(widget)
        layout.addLayout(h_layout)

        chk_layout = QHBoxLayout()
        self.chk_hours = QCheckBox("Horas")
        self.chk_minutes = QCheckBox("Minutos")
        self.chk_hours.setChecked(show_hours)
        self.chk_minutes.setChecked(show_minutes)
        chk_layout.addWidget(self.chk_hours)
        chk_layout.addWidget(self.chk_minutes)
        layout.addLayout(chk_layout)
        
        pal_layout = QHBoxLayout()
        pal_layout.addWidget(QLabel("Paleta:"))
        self.combo_palette = QComboBox()
        for name, colors in PALETTES.items():
            pixmap = QPixmap(14, 14)
            pixmap.fill(QColor(colors['arc']))
            self.combo_palette.addItem(QIcon(pixmap), name)
        self.combo_palette.setCurrentText(current_palette)
        pal_layout.addWidget(self.combo_palette)
        layout.addLayout(pal_layout)

        img_layout = QHBoxLayout()
        img_layout.addWidget(QLabel("Fondo:"))
        self.btn_img = QPushButton("Imagen Guardada" if self.bg_image and os.path.exists(self.bg_image) else "Elegir Imagen")
        self.btn_img.clicked.connect(self.select_image)
        self.btn_clear_img = QPushButton("✖")
        self.btn_clear_img.setObjectName("btn_cancel")
        self.btn_clear_img.setFixedWidth(25)
        self.btn_clear_img.clicked.connect(self.clear_image)
        img_layout.addWidget(self.btn_img)
        img_layout.addWidget(self.btn_clear_img)
        layout.addLayout(img_layout)
        
        op_layout = QHBoxLayout()
        op_layout.addWidget(QLabel("Transparencia:"))
        self.slider_opacity = QSlider(Qt.Horizontal)
        self.slider_opacity.setRange(10, 100)
        self.slider_opacity.setValue(int(current_opacity * 100))
        op_layout.addWidget(self.slider_opacity)
        layout.addLayout(op_layout)
        
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Tamaño Texto:"))
        self.slider_size = QSlider(Qt.Horizontal)
        self.slider_size.setRange(10, 80)
        self.slider_size.setValue(current_fontsize)
        size_layout.addWidget(self.slider_size)
        layout.addLayout(size_layout)

        thick_layout = QHBoxLayout()
        thick_layout.addWidget(QLabel("Grosor Borde:"))
        self.slider_thickness = QSlider(Qt.Horizontal)
        self.slider_thickness.setRange(2, 30)
        self.slider_thickness.setValue(current_thickness)
        thick_layout.addWidget(self.slider_thickness)
        layout.addLayout(thick_layout)

        appsize_layout = QHBoxLayout()
        appsize_layout.addWidget(QLabel("Tamaño App:"))
        self.slider_appsize = QSlider(Qt.Horizontal)
        self.slider_appsize.setRange(150, 400)
        self.slider_appsize.setValue(current_appsize)
        appsize_layout.addWidget(self.slider_appsize)
        layout.addLayout(appsize_layout)

        layout.addWidget(QLabel("🏳️ Banderas del Cronómetro (H:M:S):"))
        self.flag_spins = []
        grid_flags = QGridLayout()
        grid_flags.setSpacing(5)
        for i in range(5):
            f_val = current_flags[i] if i < len(current_flags) else 0
            f_h, rem_f = divmod(f_val, 3600)
            f_m, f_s = divmod(rem_f, 60)
            
            fh_spin = QSpinBox(); fh_spin.setRange(0, 99); fh_spin.setValue(f_h)
            fm_spin = QSpinBox(); fm_spin.setRange(0, 59); fm_spin.setValue(f_m)
            fs_spin = QSpinBox(); fs_spin.setRange(0, 59); fs_spin.setValue(f_s)
            
            grid_flags.addWidget(QLabel(f"#{i+1}"), i, 0)
            grid_flags.addWidget(fh_spin, i, 1)
            grid_flags.addWidget(QLabel("h"), i, 2)
            grid_flags.addWidget(fm_spin, i, 3)
            grid_flags.addWidget(QLabel("m"), i, 4)
            grid_flags.addWidget(fs_spin, i, 5)
            grid_flags.addWidget(QLabel("s"), i, 6)
            
            self.flag_spins.append((fh_spin, fm_spin, fs_spin))
        layout.addLayout(grid_flags)
        
        self.lbl_preview = QLabel("00:10:00")
        self.lbl_preview.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.lbl_preview)
        
        btn_layout = QHBoxLayout()
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setObjectName("btn_cancel")
        btn_cancel.clicked.connect(self.reject)
        
        btn_ok = QPushButton("Guardar")
        btn_ok.clicked.connect(self.accept)
        
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_ok)
        layout.addLayout(btn_layout)

        self.slider_size.valueChanged.connect(self.update_preview)
        self.combo_palette.currentTextChanged.connect(self.update_preview)
        self.chk_hours.toggled.connect(self.update_preview)
        self.chk_minutes.toggled.connect(self.update_preview)
        self.update_preview()

    def select_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Fondo", "", "Imágenes (*.png *.jpg *.jpeg *.bmp)")
        if path:
            self.bg_image = path
            self.btn_img.setText("Imagen Seleccionada")

    def clear_image(self):
        self.bg_image = None
        self.btn_img.setText("Elegir Imagen")

    def update_preview(self):
        pal = self.combo_palette.currentText()
        color = PALETTES[pal]['text']
        val = self.slider_size.value()
        self.lbl_preview.setStyleSheet(f"color: {color}; font-family: 'Consolas'; font-weight: bold; font-size: {val}px; border: none;")
        
        if self.chk_hours.isChecked():
            self.lbl_preview.setText("00:10:00")
        elif self.chk_minutes.isChecked():
            self.lbl_preview.setText("10:00")
        else:
            self.lbl_preview.setText("600")

    def get_values(self):
        seconds = self.h_spin.value() * 3600 + self.m_spin.value() * 60 + self.s_spin.value()
        flags_sec = [h.value() * 3600 + m.value() * 60 + s.value() for h, m, s in self.flag_spins]
        return (seconds, self.slider_opacity.value() / 100.0, self.combo_palette.currentText(), 
                self.slider_size.value(), self.chk_hours.isChecked(), self.chk_minutes.isChecked(), 
                self.bg_image, self.slider_thickness.value(), self.slider_appsize.value(), flags_sec)

class CuteTimer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.load_config()
        self.resize(self.app_size, self.app_size)

        self.mode = "stopwatch" 
        self.time_left = self.duration
        self.overtime = 0
        self.is_overtime = False
        self.stopwatch_time = 0
        self.is_running = False
        
        self.pulse_active = False
        self.pulse_counter = 0

        self.colors = PALETTES.get(self.current_palette_key, PALETTES["Rosa"])
        self.setWindowOpacity(self.opacity_val)

        self.update_bg_pixmap()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)

        self.init_ui()
        self.reposition_controls()
        self.oldPos = self.pos()
        
        self.setup_global_hotkey()

    def setup_global_hotkey(self):
        if sys.platform == "win32":
            self.hwnd = int(self.winId())
            ctypes.windll.user32.RegisterHotKey(self.hwnd, 1, 0x0002 | 0x0004, 0x20)

    def nativeEvent(self, event_type, message):
        if event_type == b"windows_generic_MSG":
            msg = wintypes.MSG.from_address(int(message))
            if msg.message == 0x0312:  
                if msg.wParam == 1:
                    if self.is_running:
                        self.reset_time()
                    else:
                        self.toggle_play()
                    return True, 0
        return super().nativeEvent(event_type, message)

    def closeEvent(self, event):
        if sys.platform == "win32":
            ctypes.windll.user32.UnregisterHotKey(self.hwnd, 1)
        super().closeEvent(event)

    def load_config(self):
        self.duration = 10 * 60
        self.opacity_val = 0.9
        self.current_palette_key = "Rosa"
        self.font_size = 32
        self.show_hours = True
        self.show_minutes = True
        self.bg_image = None
        self.thickness = 12
        self.app_size = 240
        self.flags = [0, 0, 0, 0, 0]

        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                self.duration = data.get("duration", self.duration)
                self.opacity_val = data.get("opacity", self.opacity_val)
                self.current_palette_key = data.get("palette", self.current_palette_key)
                self.font_size = data.get("font_size", self.font_size)
                self.show_hours = data.get("show_hours", self.show_hours)
                self.show_minutes = data.get("show_minutes", self.show_minutes)
                self.bg_image = data.get("bg_image", self.bg_image)
                self.thickness = data.get("thickness", self.thickness)
                self.app_size = data.get("app_size", self.app_size)
                self.flags = data.get("flags", self.flags)
            except Exception:
                pass

    def save_config(self):
        data = {
            "duration": self.duration,
            "opacity": self.opacity_val,
            "palette": self.current_palette_key,
            "font_size": self.font_size,
            "show_hours": self.show_hours,
            "show_minutes": self.show_minutes,
            "bg_image": self.bg_image,
            "thickness": self.thickness,
            "app_size": self.app_size,
            "flags": self.flags
        }
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception:
            pass

    def update_bg_pixmap(self):
        if self.bg_image and os.path.exists(self.bg_image):
            inner_dim = self.app_size - 20
            self.bg_pixmap = QPixmap(self.bg_image).scaled(inner_dim, inner_dim, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        else:
            self.bg_pixmap = None

    def init_ui(self):
        self.btn_play = QPushButton("▶", self)
        self.btn_play.setCursor(Qt.PointingHandCursor)
        self.btn_play.clicked.connect(self.toggle_play)

        self.btn_reset = QPushButton("⟲", self)
        self.btn_reset.setCursor(Qt.PointingHandCursor)
        self.btn_reset.clicked.connect(self.reset_time)

        self.btn_mode = QPushButton("⏳", self)
        self.btn_mode.setCursor(Qt.PointingHandCursor)
        self.btn_mode.clicked.connect(self.switch_mode)

        self.btn_menu = QPushButton("⚙", self)
        self.btn_menu.setCursor(Qt.PointingHandCursor)
        self.btn_menu.clicked.connect(self.open_config)

        self.btn_close = QPushButton("✖", self)
        self.btn_close.setCursor(Qt.PointingHandCursor)
        self.btn_close.clicked.connect(QApplication.quit)

    def reposition_controls(self):
        S = self.app_size
        btn_size = int(S * 0.125)
        if btn_size < 24: btn_size = 24
        
        radius = int(btn_size / 2)
        
        base_style = f"""
            QPushButton {{
                background-color: {self.colors['btn']};
                border-radius: {radius}px;
                color: #2b2b2b;
                font-size: {int(btn_size*0.53)}px;
                font-weight: bold;
                border: none;
            }}
            QPushButton:hover {{ background-color: {self.colors['hover']}; }}
        """
        for btn in (self.btn_play, self.btn_reset, self.btn_mode, self.btn_menu):
            btn.setStyleSheet(base_style)
            btn.setFixedSize(btn_size, btn_size)
            
        self.btn_close.setStyleSheet(base_style + """
            QPushButton { background-color: #DC143C; color: white; }
            QPushButton:hover { background-color: #B22222; }
        """)
        self.btn_close.setFixedSize(btn_size, btn_size)

        mid_x = S / 2.0
        y1 = int(S * 0.54)
        y2 = int(S * 0.70)

        self.btn_play.move(int(mid_x - (btn_size * 1.6)), y1)
        self.btn_reset.move(int(mid_x - (btn_size * 0.5)), y1)
        self.btn_mode.move(int(mid_x + (btn_size * 0.6)), y1)

        self.btn_menu.move(int(mid_x - (btn_size * 1.05)), y2)
        self.btn_close.move(int(mid_x + (btn_size * 0.05)), y2)

    def update_styles(self):
        self.reposition_controls()

    def update_time(self):
        if self.mode == "timer":
            if not self.is_overtime:
                if self.time_left > 0:
                    self.time_left -= 1
                else:
                    self.is_overtime = True
                    self.overtime += 1
            else:
                self.overtime += 1
        else:
            self.stopwatch_time += 1
            if self.stopwatch_time > 0 and self.stopwatch_time in self.flags:
                self.pulse_active = True
                self.pulse_counter = 5

        if self.pulse_active:
            if self.pulse_counter > 0:
                self.pulse_counter -= 1
            else:
                self.pulse_active = False

        self.update()

    def toggle_play(self):
        if self.is_running:
            self.timer.stop()
            self.btn_play.setText("▶")
        else:
            self.timer.start(1000)
            self.btn_play.setText("⏸")
        self.is_running = not self.is_running

    def reset_time(self):
        self.timer.stop()
        self.is_running = False
        self.btn_play.setText("▶")
        self.pulse_active = False
        self.pulse_counter = 0
        if self.mode == "timer":
            self.time_left = self.duration
            self.overtime = 0
            self.is_overtime = False
        else:
            self.stopwatch_time = 0
        self.update()

    def switch_mode(self):
        self.reset_time()
        if self.mode == "timer":
            self.mode = "stopwatch"
            self.btn_mode.setText("⏳")
        else:
            self.mode = "timer"
            self.btn_mode.setText("⏱")
        self.update()

    def open_config(self):
        dialog = ConfigDialog(self.duration, self.opacity_val, self.current_palette_key, self.font_size, self.show_hours, self.show_minutes, self.bg_image, self.thickness, self.app_size, self.flags, self)
        if dialog.exec():
            new_dur, new_op, new_pal, new_size, sh, sm, new_bg, new_thick, new_appsize, new_flags = dialog.get_values()
            
            self.app_size = new_appsize
            self.resize(self.app_size, self.app_size)

            self.opacity_val = new_op
            self.setWindowOpacity(self.opacity_val)
            self.font_size = new_size
            self.show_hours = sh
            self.show_minutes = sm
            self.thickness = new_thick
            self.flags = new_flags
            
            self.current_palette_key = new_pal
            self.colors = PALETTES[self.current_palette_key]
            
            self.bg_image = new_bg
            if self.bg_image and os.path.exists(self.bg_image):
                if not os.path.exists(ASSETS_DIR):
                    os.makedirs(ASSETS_DIR)
                ext = os.path.splitext(new_bg)[1]
                cached_bg = os.path.join(ASSETS_DIR, f"saved_bg{ext}")
                if os.path.abspath(new_bg) != os.path.abspath(cached_bg):
                    try:
                        shutil.copy2(new_bg, cached_bg)
                    except Exception:
                        pass
                self.bg_image = cached_bg
            else:
                self.bg_image = None
                
            self.update_bg_pixmap()
            self.update_styles()
            
            if new_dur > 0:
                self.duration = new_dur
                if self.mode == "timer":
                    self.time_left = self.duration
                    self.is_overtime = False
                    self.overtime = 0
            
            self.save_config()
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        S = self.app_size
        inner_dim = S - 20

        bg_color = self.colors['bg']
        arc_color = self.colors['arc']
        text_color = self.colors['text']

        is_currently_red = False
        if self.mode == "timer" and self.is_overtime:
            is_currently_red = True
        elif self.mode == "stopwatch" and self.pulse_active and (self.pulse_counter % 2 != 0):
            is_currently_red = True

        if is_currently_red:
            bg_color = "#FFD1DC" 
            arc_color = "#DC143C" 
            text_color = "#B22222" 

        painter.setPen(Qt.NoPen)
        
        if self.bg_pixmap and not (self.mode == "timer" and self.is_overtime):
            path = QPainterPath()
            path.addEllipse(10, 10, inner_dim, inner_dim)
            painter.setClipPath(path)
            px_x = 10 + (inner_dim - self.bg_pixmap.width()) // 2
            px_y = 10 + (inner_dim - self.bg_pixmap.height()) // 2
            painter.drawPixmap(px_x, px_y, self.bg_pixmap)
            painter.setClipping(False)
            
            if self.mode == "stopwatch" and self.pulse_active and (self.pulse_counter % 2 != 0):
                painter.setBrush(QColor(220, 20, 60, 80)) 
                painter.drawEllipse(10, 10, inner_dim, inner_dim)
        else:
            painter.setBrush(QColor(bg_color))
            painter.drawEllipse(10, 10, inner_dim, inner_dim)

        pen = QPen()
        pen.setWidth(self.thickness)
        pen.setColor(QColor(arc_color))
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        
        offset = 10 + (self.thickness / 2.0)
        size_dim = inner_dim - self.thickness
        rect = QRectF(offset, offset, size_dim, size_dim)
        start_angle = 90 * 16
        
        if self.mode == "timer":
            if not self.is_overtime:
                span_angle = int(-360 * 16 * (self.time_left / self.duration)) if self.duration > 0 else 0
            else:
                span_angle = -360 * 16 
        else:
            span_angle = int(-360 * 16 * ((self.stopwatch_time % 60) / 60))
            if span_angle == 0 and self.stopwatch_time > 0:
                span_angle = -360 * 16
                
        painter.drawArc(rect, start_angle, span_angle)
        
        painter.setPen(QColor(text_color))
        font = painter.font()
        font.setFamily("Consolas")
        font.setPointSize(self.font_size) 
        font.setBold(True)
        painter.setFont(font)
        
        if self.mode == "timer":
            t = self.overtime if self.is_overtime else self.time_left
        else:
            t = self.stopwatch_time
            
        h, rem = divmod(t, 3600)
        m, s = divmod(rem, 60)
        
        effective_show_hours = self.show_hours
        effective_show_minutes = self.show_minutes
        
        if self.mode == "stopwatch" and t >= 3600:
            effective_show_hours = True
            effective_show_minutes = True

        parts = []
        if effective_show_hours:
            parts.extend([f"{h:02d}", f"{m:02d}", f"{s:02d}"])
        elif effective_show_minutes:
            total_m = h * 60 + m
            parts.extend([f"{total_m:02d}", f"{s:02d}"])
        else:
            total_s = h * 3600 + m * 60 + s
            parts.append(f"{total_s:02d}")
            
        time_str = ":".join(parts)
        
        if self.is_overtime and self.mode == "timer":
            time_str = "+" + time_str
            
        painter.drawText(QRectF(10, int(S * 0.15), inner_dim, int(S * 0.35)), Qt.AlignCenter, time_str)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = event.globalPosition().toPoint() - self.oldPos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPosition().toPoint()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    timer = CuteTimer()
    timer.show()
    sys.exit(app.exec())