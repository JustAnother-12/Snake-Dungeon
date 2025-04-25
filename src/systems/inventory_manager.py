

import time
import pygame
from entities.items.item_stack import ItemStack
from entities.items.item_type import ActivationType, ItemCategory
from entities.items.skill.thanos import ThanosEntity


class InventoryManager:
    from entities import Player

    def __init__(self, snake: "Player.Snake") -> None:

        self.slots: list[ItemStack | None] = [
            None, None, None, None, None, None]
        self.slots_map_type = [
            ItemCategory.CONSUMABLE,
            ItemCategory.CONSUMABLE,
            ItemCategory.EQUIPMENT,
            ItemCategory.EQUIPMENT,
            ItemCategory.EQUIPMENT,
            ItemCategory.SKILL
        ]
        self.snake = snake
        self.keys_map = [
            pygame.K_1,
            pygame.K_2,
            pygame.K_3,
            pygame.K_4,
            pygame.K_5,
            pygame.K_LCTRL
        ]
        self.keys_pressed = {key: False for key in self.keys_map}
        # list check key pressed
        # 1, 2, 3, 4, 5, Ctrl
        self.time_press: list[float] = [0, 0, 0, 0, 0, 0]
        self.press_time = 0.5
        # list check key pressed for Konami Code
        self.key_pressed_history = [0, 0, 0, 0, 0, 0, 0, 0]

    def count_slots(self):
        skill_count = 0
        consumable_count = 0
        equipment_count = 0
        for item in self.slots:
            if item is not None:
                if item.item_type.category == ItemCategory.CONSUMABLE:
                    consumable_count += 1
                elif item.item_type.category == ItemCategory.EQUIPMENT:
                    equipment_count += 1
                else:
                    skill_count += 1
        return skill_count, consumable_count, equipment_count

    def handle_key_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.key_pressed_history.append(event.key)
            self.key_pressed_history.pop(0)
            for index, key in enumerate(self.keys_map):
                if event.key == key:
                    self.keys_pressed[key] = True
                    self.time_press[index] = time.time()
                    # Đánh dấu item là active khi nhấn
                    if not self.slots[index] is None:
                        self.slots[index].active = True  # type: ignore

        elif event.type == pygame.KEYUP:
            for index, key in enumerate(self.keys_map):
                if event.key == key:
                    self.keys_pressed[key] = False
                    # Nếu thời gian nhấn ngắn, sử dụng item
                    if self.time_press[index] > 0:
                        press_duration = time.time() - self.time_press[index]
                        if press_duration < self.press_time:
                            if not self.slots[index] is None:
                                self.slots[index].use(self.snake)  # type: ignore
                        self.time_press[index] = 0
                    if not self.slots[index] is None:
                        self.slots[index].active = False  # type: ignore

    # Thay đổi phương thức update để kiểm tra phím giữ
    def update(self):

        # kiểm tra phím giữ co phai la konami code hay không
        # print(self.key_pressed_history)
        if (
            self.key_pressed_history[0] == pygame.K_UP and
            self.key_pressed_history[1] == pygame.K_UP and
            self.key_pressed_history[2] == pygame.K_DOWN and
            self.key_pressed_history[3] == pygame.K_DOWN and
            self.key_pressed_history[4] == pygame.K_LEFT and
            self.key_pressed_history[5] == pygame.K_RIGHT and
            self.key_pressed_history[6] == pygame.K_LEFT and
            self.key_pressed_history[7] == pygame.K_RIGHT
        ):
            print("Konami code detected!")
            self.key_pressed_history = [0, 0, 0, 0, 0, 0, 0, 0]
            self.snake.level.item_group.add(
                ThanosEntity(self.snake.level, self.snake.blocks[1].rect, 2))
            # Thực hiện hành động tương ứng với việc phát hiện Konami code

        current_time = time.time()
        for index, key in enumerate(self.keys_map):
            # Kiểm tra nếu phím đang được giữ và đã giữ đủ lâu
            if self.keys_pressed[key] and self.time_press[index] > 0:
                if current_time - self.time_press[index] > self.press_time:
                    # Drop item khi giữ phím đủ lâu
                    if not self.slots[index] is None:
                        self.drop(index)
                        # Reset thời gian để tránh drop liên tục
                        self.time_press[index] = 0
                        self.keys_pressed[key] = False

        # Cập nhật các item trong inventory
        for value in self.slots:
            if value is None:
                continue
            value.update(self)

    def _check_item_exits(self, item: ItemStack):
        '''chả về vị trị của item đó trong mảng Không thấy thì nó trả về -1'''
        for index, value in enumerate(self.slots):
            if value is None:
                continue

            if value.item_type.id == item.item_type.id:
                return index

        return -1

    def add_item(self, item: ItemStack) -> bool:

        # nếu item đã tồn tại
        index = self._check_item_exits(item)
        if index >= 0:
            if item.item_type.category == ItemCategory.EQUIPMENT:
                return False

            return self.slots[index].stack(item)  # type: ignore

        # tìm lot trống
        for index, value in enumerate(self.slots):

            # bỏ qua những slot khác loại
            if self.slots_map_type[index] != item.item_type.category:
                continue

            if value is None:
                self.slots[index] = item
                if item.item_type.activation_type == ActivationType.ON_PICKUP:
                    # tự động kích hoạt hiệu ứng nếu là equipment
                    item.apply_effect(self.snake)
                return True

        return False

    def remove_item(self, item: ItemStack, quantity: int = -1):
        index = self._check_item_exits(item)
        if index < 0:
            return False

        
        if quantity == -1 or (self.slots[index].quantity - quantity) == 0: # type: ignore
            self.slots[index] = None
            return True

        if self.slots[index].quantity - quantity < 0:  # type: ignore
            return False

        self.slots[index].quantity -= quantity  # type: ignore

    def drop(self, index: int):
        # self.snake.level.item_group.add(ItemEntity())
        if self.slots[index] is None:
            return False
        elif self.slots[index].get_cooldown_remaining() > 0:  # type:ignore
            return False

        if self.slots[index].item_type.category == ItemCategory.EQUIPMENT:  # type: ignore
            self.slots[index].remove_effect(self.snake)  # type: ignore

        
        item_entity_class = self.slots[index].get_item_entity_class() # type: ignore
        self.snake.level.item_group.add(item_entity_class(
            
            self.snake.level, self.snake.blocks[1].rect, 2, self.slots[index].quantity)) # type: ignore
        self.slots[index] = None
        return True
