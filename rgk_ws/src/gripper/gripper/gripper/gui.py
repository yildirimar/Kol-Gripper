#!/usr/bin/env python3
import sys
import tkinter as tk
from tkinter import ttk
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray

class GripperGUI(Node):
    def __init__(self):
        super().__init__('gripper_gui_node')
        
        self.publisher_ = self.create_publisher(
            Float64MultiArray, 
            '/gripper_controller/commands', 
            10
        )
        
        self.MIN_LIMIT = -0.08 
        self.MAX_LIMIT = 0.04   
        
        self.root = tk.Tk()
        self.root.title("Gripper Control Panel") 
        self.root.geometry("400x200")
        
    
        lbl_title = tk.Label(self.root, text="Gripper Controller", font=("Arial", 16, "bold"))
        lbl_title.pack(pady=10)

        self.lbl_value = tk.Label(self.root, text="Konum: 0.00 m", font=("Arial", 12))
        self.lbl_value.pack(pady=5)

        self.slider = tk.Scale(
            self.root, 
            from_=self.MIN_LIMIT * 100, 
            to=self.MAX_LIMIT * 100, 
            orient='horizontal', 
            length=300,
            resolution=0.1,
            command=self.on_slider_change
        )
        self.slider.set(0.04 * 100)
        self.slider.pack(pady=20)

        btn_exit = tk.Button(self.root, text="Kapat", command=self.close_app, bg="red", fg="white")
        btn_exit.pack(pady=10)

        self.root.mainloop()

    def on_slider_change(self, val):
        pos_meter = float(val) / 100.0
        self.lbl_value.config(text=f"Konum: {pos_meter:.3f} m")
        
        msg = Float64MultiArray()
        msg.data = [pos_meter, pos_meter]
        self.publisher_.publish(msg)

    def close_app(self):
        self.root.destroy()
        self.destroy_node()
        rclpy.shutdown()

def main():
    rclpy.init()
    app = GripperGUI()

if __name__ == '__main__':
    main()