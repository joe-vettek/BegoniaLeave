// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

// Learn more about Tauri commands at https://tauri.app/v1/guides/features/command
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}
use std::process::{Command, Stdio};
use std::os::windows::process::CommandExt;
fn main() {
	// 我们现在不再需要通过rs便携cmd程序了，通过js就可以完成这个工作
 // let _output = Command::new("cmd.exe")
 // //.creation_flags(0x08000000)
 //        .arg("/C") // Run the command and then terminate
 //        .arg(r"bin\python\python.exe webapp.py")
 //        .arg(r"pause")
 //        //.stdin(Stdio::piped()) // Set up stdin
 //        .spawn();
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
