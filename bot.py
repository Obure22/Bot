import ctypes
import time
import cv2
import keyboard
import win32api
import win32con
import win32gui
from PIL import ImageGrab, Image
from keyboard import mouse
from numpy import array, uint8, zeros_like



def find_window_by_title(title):
    hwnd = win32gui.FindWindow(None, title)
    return hwnd

def get_window_size(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    left, top, right, bottom = rect
    width = right - left
    height = bottom - top
    return width,height

def get_window_cords(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    left, top, right, bottom = rect
    return left,top,right,bottom


def correct_show_image_debug(img):
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    mask = cv2.inRange(img_bgr, array([243, 160, 105]), array([253, 180, 130]))
    # Применение маски к изображению

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
    morph_result = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(morph_result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        rect_image = zeros_like(img_bgr)
        cv2.rectangle(rect_image, (x, y), (x + w, y + h), (255, 255, 255), -1)  # Прямоугольник белого цвета
        result = cv2.bitwise_and(img_bgr, rect_image)

    cv2.imshow('Screen Capture', result)
    cv2.waitKey(0)  # Ожидание нажатия клавиши
    cv2.destroyAllWindows()  # Закрытие окна


def get_screen(x1, y1, x2, y2):
    box = (x1, y1, x2, y2)
    while True:
        screen = ImageGrab.grab(box)
        img = array(screen.getdata(), dtype=uint8).reshape((screen.size[1], screen.size[0], 3))
        yield img

def correct_show_image(img):
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    mask = cv2.inRange(img_bgr, array([243, 160, 105]), array([253, 180, 130]))
    # Применение маски к изображению

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
    morph_result = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(morph_result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        rect_image = zeros_like(img_bgr)
        cv2.rectangle(rect_image, (x, y), (x + w, y + h), (255, 255, 255), -1)  # Прямоугольник белого цвета
        result = cv2.bitwise_and(img_bgr, rect_image)
    center_x = (x+(x+w))//2
    return center_x



def control_player(center_box_x,centerScreenX,hwnd):
    game_window = hwnd
    if game_window == win32gui.GetForegroundWindow():
        if abs(center_box_x-centerScreenX)<60:
            mouse.move(centerScreenX, 600)

            print("по центру")




stop_program = False  # Флаг для остановки программы
def on_key_event(event):
    global stop_program
    if event.name == 'q':
        stop_program = True  # Устанавливаем флаг, когда нажата 'q'
keyboard.on_press(on_key_event)


if __name__ == "__main__":
    window_title = "Skyrim"
    hwnd = find_window_by_title(window_title)
    print(f"Найдено окно: {hwnd}")
    size=get_window_size(hwnd)
    centerScreenX = int(size[0]/2)
    print(size)
    print(centerScreenX)
    left,top,right,bottom= get_window_cords(hwnd)
    print(left,top,right,bottom)
    imgs = get_screen(left,top,right,bottom)


    for img in imgs:
        if stop_program:
            break
        center_box_x = correct_show_image(img)
        control_player(center_box_x,centerScreenX,hwnd)





        #if keyboard.is_pressed('q'):
           # break



#mask = cv2.inRange(img_bgr, array([220, 110, 60]), array([255, 205, 150]))

#mask = cv2.inRange(img_bgr, array([243, 160, 105]), array([253, 180, 130]))