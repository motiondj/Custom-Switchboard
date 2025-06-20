# Copyright Epic Games, Inc. All Rights Reserved.

import json
import os
from pathlib import Path
from typing import Optional, Callable

from PySide6 import QtCore, QtGui, QtWidgets

from switchboard import config
from switchboard.switchboard_logging import LOGGER


class ConfigListItem(QtWidgets.QListWidgetItem):
    """Config 파일을 나타내는 리스트 아이템"""
    
    def __init__(self, config_path: Path, parent=None):
        super().__init__(parent)
        self.config_path = config_path
        self.config_data = None
        
        # 기본 정보 설정
        self.setText(config_path.stem)
        self.setToolTip(str(config_path))
        
        # 아이콘 설정
        self.setIcon(QtGui.QIcon(":/icons/images/icon_settings.png"))
        
        # Config 데이터 로드
        self.load_config_data()
    
    def load_config_data(self):
        """Config 파일의 데이터를 로드합니다"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config_data = json.load(f)
        except Exception as e:
            LOGGER.warning(f"Failed to load config {self.config_path}: {e}")
            self.config_data = None
    
    def get_project_name(self) -> str:
        """프로젝트 이름을 반환합니다"""
        if self.config_data and 'project_name' in self.config_data:
            return self.config_data['project_name']
        return self.config_path.stem
    
    def get_device_count(self) -> int:
        """디바이스 개수를 반환합니다"""
        if self.config_data and 'devices' in self.config_data:
            device_count = 0
            for device_type, device_data in self.config_data['devices'].items():
                if isinstance(device_data, dict):
                    # 개별 디바이스들 (예: nDisplay의 Node_0, Node_1 등)
                    for device_name, device_settings in device_data.items():
                        if device_name != 'settings':  # settings는 제외
                            device_count += 1
                    # 플러그인 레벨 설정이 있는 경우
                    if 'settings' in device_data:
                        device_count += 1
                else:
                    device_count += 1
            return device_count
        return 0
    
    def get_device_types(self) -> list:
        """디바이스 타입들을 반환합니다"""
        if self.config_data and 'devices' in self.config_data:
            return list(self.config_data['devices'].keys())
        return []


class ConfigBrowserWidget(QtWidgets.QWidget):
    """Config 파일들을 브라우징하는 위젯"""
    
    signal_config_selected = QtCore.Signal(Path)
    signal_config_activate_requested = QtCore.Signal(Path)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 폰트 설정
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.setFont(font)
        
        # 레이아웃 설정
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(10, 10, 10, 10)
        self.layout().setSpacing(10)
        
        self.setup_ui()
        self.refresh_config_list()
        
        # Config 리스트 스타일 설정
        self.config_list.setStyleSheet("""
            QListWidget {
                border: none;
                background-color: transparent;
            }
            QListWidget::item {
                background-color: #3d3d3d;
                color: #d8d8d8;
                border-radius: 6px;
                padding: 8px;
                margin: 2px 0px;
            }
            /* 짝수/홀수 행 색상 동일하게 */
            QListWidget::item:alternate {
                background-color: #3d3d3d;
            }
            QListWidget::item:hover {
                background-color: #4a4a4a;
            }
            QListWidget::item:selected {
                background-color: #520000;
                border: 1px solid #ff5603;
            }
        """)
    
    def setup_ui(self):
        """UI를 설정합니다"""
        layout = self.layout()
        
        # 헤더
        header_layout = QtWidgets.QHBoxLayout()
        
        title_label = QtWidgets.QLabel("Configuration Files")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # 새로고침 버튼
        refresh_button = QtWidgets.QPushButton()
        refresh_button.setIcon(QtGui.QIcon(":/icons/images/icon_refresh.png"))
        refresh_button.setToolTip("Refresh config list")
        refresh_button.clicked.connect(self.refresh_config_list)
        header_layout.addWidget(refresh_button)
        
        layout.addLayout(header_layout)
        
        # 검색 필터
        filter_layout = QtWidgets.QHBoxLayout()
        filter_layout.addWidget(QtWidgets.QLabel("Search:"))
        
        self.search_edit = QtWidgets.QLineEdit()
        self.search_edit.setPlaceholderText("Search config files...")
        self.search_edit.textChanged.connect(self.filter_configs)
        filter_layout.addWidget(self.search_edit)
        
        layout.addLayout(filter_layout)
        
        # Config 리스트
        self.config_list = QtWidgets.QListWidget()
        self.config_list.setAlternatingRowColors(False)
        self.config_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.config_list.itemDoubleClicked.connect(self.on_config_double_clicked)
        self.config_list.itemSelectionChanged.connect(self.on_selection_changed)
        self.config_list.setToolTip("Click: Load config only\nDouble-click: Load config and launch all devices")
        layout.addWidget(self.config_list)
        
        # 미리보기 패널
        preview_group = QtWidgets.QGroupBox("Preview")
        preview_layout = QtWidgets.QVBoxLayout(preview_group)
        
        self.preview_text = QtWidgets.QTextEdit()
        self.preview_text.setMaximumHeight(150)
        self.preview_text.setReadOnly(True)
        preview_layout.addWidget(self.preview_text)
        
        layout.addWidget(preview_group)
        
        # 버튼들
        button_layout = QtWidgets.QHBoxLayout()
        
        self.load_button = QtWidgets.QPushButton("Load Selected Config")
        self.load_button.clicked.connect(self.load_selected_config)
        self.load_button.setEnabled(False)
        button_layout.addWidget(self.load_button)
        
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
    
    def refresh_config_list(self):
        """Config 파일 목록을 새로고침합니다"""
        self.config_list.clear()
        
        try:
            config_paths = config.list_config_paths()
            
            for config_path in config_paths:
                # user_settings.json은 제외
                if config_path.name == 'user_settings.json':
                    continue
                    
                item = ConfigListItem(config_path, self.config_list)
                self.config_list.addItem(item)
            
            # 파일명으로 정렬
            self.config_list.sortItems()
            
            # 현재 로드된 config 하이라이트
            self.highlight_current_config()
            
        except Exception as e:
            LOGGER.error(f"Failed to refresh config list: {e}")
    
    def highlight_current_config(self):
        """현재 로드된 config 파일을 하이라이트합니다"""
        try:
            from switchboard.config import SETTINGS
            current_config_path = SETTINGS.CONFIG
            
            if current_config_path:
                current_config_path = Path(current_config_path)
                
                for i in range(self.config_list.count()):
                    item = self.config_list.item(i)
                    if isinstance(item, ConfigListItem):
                        if item.config_path == current_config_path:
                            # 현재 config를 선택 상태로 설정
                            self.config_list.setCurrentItem(item)
                            # 배경색을 다르게 설정
                            item.setBackground(QtGui.QColor(100, 150, 255, 100))
                            break
        except Exception as e:
            LOGGER.warning(f"Failed to highlight current config: {e}")
    
    def on_config_selected(self, config_path: Path):
        """Config가 선택되었을 때 하이라이트를 업데이트합니다"""
        # 모든 아이템의 배경색을 초기화
        for i in range(self.config_list.count()):
            item = self.config_list.item(i)
            if isinstance(item, ConfigListItem):
                item.setBackground(QtGui.QColor(0, 0, 0, 0))  # 투명
        
        # 선택된 config를 하이라이트
        for i in range(self.config_list.count()):
            item = self.config_list.item(i)
            if isinstance(item, ConfigListItem):
                if item.config_path == config_path:
                    item.setBackground(QtGui.QColor(100, 150, 255, 100))
                    break
    
    def filter_configs(self, text: str):
        """Config 파일들을 필터링합니다"""
        for i in range(self.config_list.count()):
            item = self.config_list.item(i)
            if isinstance(item, ConfigListItem):
                # 파일명이나 프로젝트명으로 검색
                matches = (text.lower() in item.text().lower() or 
                          text.lower() in item.get_project_name().lower())
                item.setHidden(not matches)
    
    def on_config_double_clicked(self, item: ConfigListItem):
        """Config를 더블클릭했을 때 호출됩니다 - config 로드 후 모든 디바이스 연결 및 실행"""
        LOGGER.info(f"Config activation requested: {item.config_path.name}")
        self.signal_config_activate_requested.emit(item.config_path)
    
    def on_selection_changed(self):
        """리스트에서 선택이 변경되었을 때 호출됩니다"""
        current_item = self.config_list.currentItem()
        if isinstance(current_item, ConfigListItem):
            self.load_button.setEnabled(True)
            self.update_preview(current_item)
            
            # 한 번 클릭 시 config 로드 (실행하지 않음)
            self.load_config(current_item.config_path)
        else:
            self.load_button.setEnabled(False)
            self.preview_text.clear()
    
    def load_selected_config(self):
        """선택된 config를 로드합니다"""
        current_item = self.config_list.currentItem()
        if isinstance(current_item, ConfigListItem):
            self.load_config(current_item.config_path)
    
    def load_config(self, config_path: Path):
        """Config를 로드합니다"""
        # 하이라이트 업데이트
        self.on_config_selected(config_path)
        
        # 시그널 발생
        self.signal_config_selected.emit(config_path)
    
    def update_preview(self, item: ConfigListItem):
        """Config 미리보기를 업데이트합니다"""
        if not item.config_data:
            self.preview_text.setText("Failed to load config data")
            return
        
        preview_text = []
        preview_text.append(f"<b>Project:</b> {item.get_project_name()}")
        preview_text.append(f"<b>File:</b> {item.config_path.name}")
        preview_text.append(f"<b>Devices:</b> {item.get_device_count()}")
        
        device_types = item.get_device_types()
        if device_types:
            preview_text.append(f"<b>Device Types:</b> {', '.join(device_types)}")
        
        # 엔진 정보
        if 'engine_dir' in item.config_data:
            engine_dir = item.config_data['engine_dir']
            if engine_dir:
                engine_name = Path(engine_dir).name if engine_dir else "Unknown"
                preview_text.append(f"<b>Engine:</b> {engine_name}")
        
        # 멀티유저 서버 정보
        if 'muserver_server_name' in item.config_data:
            mu_server = item.config_data['muserver_server_name']
            if mu_server:
                preview_text.append(f"<b>MU Server:</b> {mu_server}")
        
        self.preview_text.setHtml("<br>".join(preview_text)) 