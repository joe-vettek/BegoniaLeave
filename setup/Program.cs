using System;
using System.Diagnostics;
using System.IO;
using System.IO.Compression;
using System.Net;
using System.Resources;
using BegoniaLeaveSetup;
using System.IO;
namespace WinFormsApp
{
    internal static class Program
    {
        /// <summary>
        ///  The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            // To customize application configuration such as set high DPI settings or default font,
            // see https://aka.ms/applicationconfiguration.
            ApplicationConfiguration.Initialize();
            // URL of the gzipped file you want to download
            string fileUrl = "https://mirrors.huaweicloud.com/python/3.8.10/python-3.8.10-embed-amd64.zip";
            string downloadPath = "python-3.8.10-embed-amd64.zip"; // Specify the local path to save the downloaded file

            // Download the gzipped file using WebClient
            using (WebClient client = new WebClient())
            {
                client.DownloadFile(fileUrl, downloadPath);
            }

            // Decompress the downloaded gzipped file
            string extractedFilePath = "bin/python"; // 解压后的文件路径

            try
            {
                ZipFile.ExtractToDirectory(downloadPath, extractedFilePath);
                string filePath = "bin/python/python38._pth"; // 替换为你自己的文件路径
                string textToWrite = "python38.zip\r\n.\r\n\r\n# Uncomment to run site.main() automatically\r\nimport site";
                File.WriteAllText(filePath, textToWrite);
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }

            string pipFileUrl = "https://bootstrap.pypa.io/get-pip.py";
            string endPath = "bin/python/get-pip.py"; // Specify the local path to save the downloaded file

            // 加载资源文件
            //ResourceManager resourceManager = new ResourceManager("pip.get_pip", typeof(pip).Assembly);Assembly.GetExecutingAssembly()
            // 创建ResourceManager实例
            ResourceManager rm = new ResourceManager("BegoniaLeaveSetup.Pip", typeof(Pip).Assembly);

            // 读取资源
            byte[] stream = (byte[])rm.GetObject("get_pip");
            /* using (StreamReader reader = new StreamReader(stream))
             {
                 string text = reader.ReadToEnd();
                 File.WriteAllText(endPath, text);
             }*/
            File.WriteAllBytes(endPath, stream);

            Console.WriteLine("Downloaded and decompressed successfully!");

            string pythonPath = "bin/python/python.exe"; // Specify the local path to save the downloaded file​

            Process p = new Process();
            //设置要启动的应用程序
            p.StartInfo.FileName = "cmd.exe";
            //是否使用操作系统shell启动
            p.StartInfo.UseShellExecute = false;
            // 接受来自调用程序的输入信息
            p.StartInfo.RedirectStandardInput = true;
            //输出信息
            p.StartInfo.RedirectStandardOutput = false;
            // 输出错误
            p.StartInfo.RedirectStandardError = true;
            //不显示程序窗口
            p.StartInfo.CreateNoWindow = false;
            //启动程序
            p.Start();

            p.StandardInput.WriteLine($"\"{Path.GetFullPath(pythonPath)}\" \"{Path.GetFullPath(endPath)}\" -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn");
           

            string requirementPath = "bin/python/requirement.txt"; // Specify the local path to save the downloaded file
            string requirementTxt = rm.GetString("requirement");
            File.WriteAllText(requirementPath, requirementTxt);
            string[] requires= requirementTxt.Split("\n");
            foreach(string s in requires)
            {
                p.StandardInput.WriteLine($"\"{Path.GetFullPath(pythonPath)}\" -m pip install \"{s}\" -i https://pypi.tuna.tsinghua.edu.cn/simple");
            }
            //p.StandardInput.WriteLine($"\"{Path.GetFullPath(pythonPath)}\" -m pip install -r \"{Path.GetFullPath(requirementPath)}\" -i https://pypi.tuna.tsinghua.edu.cn/simple");
            //p.StandardInput.WriteLine($"\"{Path.GetFullPath(pythonPath)}\" -m pip install uvicorn -i https://pypi.tuna.tsinghua.edu.cn/simple");
            //p.StandardInput.WriteLine($"\"{Path.GetFullPath(pythonPath)}\" -m pip install fastapi -i https://pypi.tuna.tsinghua.edu.cn/simple");
            //p.StandardInput.WriteLine($"\"{Path.GetFullPath(pythonPath)}\" -m pip install adbutils -i https://pypi.tuna.tsinghua.edu.cn/simple");
            //p.StandardInput.WriteLine($"\"{Path.GetFullPath(pythonPath)}\" -m pip install uiautomator2 -i https://pypi.tuna.tsinghua.edu.cn/simple");
            //p.StandardInput.WriteLine($"\"{Path.GetFullPath(pythonPath)}\" -m pip install paddlepaddle -i https://pypi.tuna.tsinghua.edu.cn/simple");
            //p.StandardInput.WriteLine($"\"{Path.GetFullPath(pythonPath)}\" -m pip install paddleocr -i https://pypi.tuna.tsinghua.edu.cn/simple");
            //p.StandardInput.WriteLine($"\"{Path.GetFullPath(pythonPath)}\" -m pip install Pyside6 -i https://pypi.tuna.tsinghua.edu.cn/simple");
            p.StandardInput.AutoFlush = true;

            File.WriteAllText("_re_install.bat", $"\"{Path.GetFullPath(pythonPath)}\" -m pip install -r \"{Path.GetFullPath(requirementPath)}\" -i https://pypi.tuna.tsinghua.edu.cn/simple");
            //获取输出信息
            //string strOuput = p.StandardOutput.ReadToEnd();
            //等待程序执行完退出进程
            p.WaitForExit();
            p.Close();
            Console.WriteLine("");

            Application.Run(new Form1());
        }
    }
}