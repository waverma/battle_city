from battle_city.buffers.buffer_to_game_logic import BufferToGameLogic
from battle_city.buffers.buffer_to_render import BufferToRender
from battle_city.buffers.drawing_buffer import DrawingBuffer
from battle_city.buffers.user_event import UserEvent
from battle_city.enums import InterfaceStage
from battle_city.view.graphic_utils import GraphicUtils
from battle_city.view.gui_elements.game_field_element import (
    GameFieldElement,
)
from battle_city.view.gui_elements.menus.main_menu import MainMenu
from battle_city.view.gui_elements.menus.pause_menu import (
    PauseMenu,
)
from battle_city.view.gui_elements.menus.post_game_after_win_menu \
    import (
        PostGameAfterWinMenu,
    )
from battle_city.view.gui_elements.menus.post_game_element import (
    PostGameElement,
)
from battle_city.view.gui_elements.menus.single_play_menu import (
    SinglePlayMenu,
)


def render_per_element(buffer_to_render, new_buffer_to_draw, element):
    render_info = element.get_render_info((0, 0, 1, 1), buffer_to_render)
    for render_info_parts in render_info:
        new_buffer_to_draw.add(render_info_parts)


class UserInterface:
    def __init__(self):
        self.elements = list()
        self.stage = InterfaceStage.MainMenu

        # Создание менюшек
        self.game_field_element = GameFieldElement(
            GraphicUtils.DEFAULT_GAME_FIELD_ELEMENT_COLLISION, (0, 0)
        )
        self.post_game_menu = PostGameElement(
            GraphicUtils.DEFAULT_MENU_COLLISION, (0, 0)
        )
        self.post_game_after_win_menu = PostGameAfterWinMenu(
            GraphicUtils.DEFAULT_MENU_COLLISION, (0, 0)
        )
        self.main_menu = MainMenu(GraphicUtils.DEFAULT_MENU_COLLISION, (0, 0))
        self.single_menu = SinglePlayMenu(
            GraphicUtils.DEFAULT_MENU_COLLISION, (0, 0)
        )
        self.pause = PauseMenu(GraphicUtils.DEFAULT_MENU_COLLISION, (0, 0))

    def update(
        self,
        e: UserEvent,
        game_state: InterfaceStage,
        output_buffer: BufferToGameLogic,
    ):
        output_buffer.interface_stage = game_state
        output_buffer.is_cancel_button_pressed = False

        if game_state == InterfaceStage.MainMenu:
            self.main_menu.update(e, output_buffer)

        elif game_state == InterfaceStage.InGame:
            self.game_field_element.update(e, output_buffer)

        elif game_state == InterfaceStage.Pause:
            self.pause.update(e, output_buffer)

        elif game_state == InterfaceStage.PostGame:
            self.post_game_menu.update(e, output_buffer)

        elif game_state == InterfaceStage.PostGameAfterWin:
            self.post_game_after_win_menu.update(e, output_buffer)

        elif game_state == InterfaceStage.SinglePlayMenu:
            self.single_menu.update(e, output_buffer)

    def render(
        self, buffer_to_render: BufferToRender, buffer_to_draw: DrawingBuffer
    ):
        # new_buffer_to_draw = DrawingBuffer()
        new_buffer_to_draw = buffer_to_draw

        self.stage = buffer_to_render.game_stage

        if self.stage == InterfaceStage.MainMenu:
            render_per_element(
                buffer_to_render, new_buffer_to_draw, self.main_menu
            )

        elif self.stage == InterfaceStage.InGame:
            self.game_field_element.get_render_info(
                (0, 0, 1, 1), buffer_to_render, new_buffer_to_draw
            )
        #     for render_info_parts in render_info:
        #         new_buffer_to_draw.add(render_info_parts)

        elif self.stage == InterfaceStage.PostGame:
            render_per_element(
                buffer_to_render, new_buffer_to_draw, self.post_game_menu
            )

        elif self.stage == InterfaceStage.PostGameAfterWin:
            render_per_element(
                buffer_to_render,
                new_buffer_to_draw,
                self.post_game_after_win_menu,
            )

        elif self.stage == InterfaceStage.SinglePlayMenu:
            render_per_element(
                buffer_to_render, new_buffer_to_draw, self.single_menu
            )

        elif self.stage == InterfaceStage.Pause:
            render_per_element(
                buffer_to_render, new_buffer_to_draw, self.pause
            )

        # buffer_to_draw.update(new_buffer_to_draw)
