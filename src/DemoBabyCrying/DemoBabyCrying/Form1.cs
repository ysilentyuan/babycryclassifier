using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace DemoBabyCrying
{
    public partial class Form1 : Form
    {
        private string GetStartRecordExePath()
        {
            return Path.Combine(GetCurrentExeDirectoryPath(), "sound_recognizer.exe");
        }

        private string GetEndRecordExePath()
        {
            return Path.Combine(GetCurrentExeDirectoryPath(), "stop_record.exe");
        }

        private string GetCreateCSVExePath()
        {
            return Path.Combine(GetCurrentExeDirectoryPath(), "abstractor", "abstractor.exe");
        }

        private string GetPredictExePath()
        {
            return Path.Combine(GetCurrentExeDirectoryPath(), "predictor.exe");
        }

        private string GetCSVFilePath()
        {
            return Path.Combine(GetCurrentExeDirectoryPath(), "test.csv");
        }

        private string GetResFilePath()
        {
            return Path.Combine(GetCurrentExeDirectoryPath(), "test.txt");
        }

        private string GetPredictResPath()
        {
            return Path.Combine(GetCurrentExeDirectoryPath(), "result.txt");
        }

        private string GetAudioPath()
        {
            return Path.Combine(GetCurrentExeDirectoryPath(), "test.wav");
        }
        
        private  string GetCurrentExeDirectoryPath()
        {
            return  Directory.GetCurrentDirectory();
        }

        public Form1()
        {
            InitializeComponent();
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void startRecordBtn_Click(object sender, EventArgs e)
        {
            ProcessStartInfo startInfor = new ProcessStartInfo();
            startInfor.CreateNoWindow = false;
            startInfor.UseShellExecute = false;
            startInfor.FileName = GetStartRecordExePath();
            startInfor.WindowStyle = ProcessWindowStyle.Hidden;
            startInfor.Arguments = GetAudioPath();

            try
            {
                using (Process startRecordProc = Process.Start(startInfor))
                {
                }
            }
            catch (Exception exp)
            {
                System.Windows.Forms.MessageBox.Show(exp.Message);
            }
        }

        private void endRecordBtn_Click(object sender, EventArgs e)
        {
            var result = Jacksonsoft.WaitWindow.Show(
            (s, waitEvent) =>
            {
                ProcessStartInfo startInfor = new ProcessStartInfo();
                startInfor.CreateNoWindow = false;
                startInfor.UseShellExecute = false;
                startInfor.FileName = GetEndRecordExePath();
                startInfor.WindowStyle = ProcessWindowStyle.Hidden;

                try
                {
                    using (Process endRecordProc = Process.Start(startInfor))
                    {
                        endRecordProc.WaitForExit();
                    }
                    waitEvent.Result = "Done";
                }
                catch (Exception exp)
                {
                    System.Windows.Forms.MessageBox.Show(exp.Message);
                }
                finally
                {
                    CreateCSVFile();
                }
            }, "Please wait for analyzing...");
        }

        private void CreateCSVFile()
        {
            ProcessStartInfo startInfor = new ProcessStartInfo();
            startInfor.CreateNoWindow = false;
            startInfor.UseShellExecute = false;
            startInfor.FileName = GetCreateCSVExePath();
            startInfor.WindowStyle = ProcessWindowStyle.Hidden;
            startInfor.Arguments = GetAudioPath() + " " + GetCSVFilePath();

            try
            {
                using (Process proc = Process.Start(startInfor))
                {
                    proc.WaitForExit();
                }
            }
            catch (Exception exp)
            {
                System.Windows.Forms.MessageBox.Show(exp.Message);
            }

            finally
            {
                CreateBabyCryingAnalysis();
            }
        }

        private void CreateBabyCryingAnalysis()
        {
            ProcessStartInfo startInfor = new ProcessStartInfo();
            startInfor.CreateNoWindow = false;
            startInfor.UseShellExecute = false;
            startInfor.FileName = GetCreateCSVExePath();
            startInfor.WindowStyle = ProcessWindowStyle.Hidden;
            startInfor.Arguments = GetCSVFilePath() + " " + GetResFilePath();

            ProcessStartInfo startPredictor = new ProcessStartInfo();
            startPredictor.CreateNoWindow = false;
            startPredictor.UseShellExecute = false;
            startPredictor.FileName = GetPredictExePath();
            startPredictor.WindowStyle = ProcessWindowStyle.Hidden;
            startPredictor.Arguments = GetCSVFilePath() + " " + GetPredictResPath();
            try
            {
                using (Process proc = Process.Start(startInfor))
                {
                    proc.WaitForExit();
                }
                using (Process proc = Process.Start(startPredictor))
                {
                    proc.WaitForExit();
                }
                using (var sr = new StreamReader(Path.Combine(GetCurrentExeDirectoryPath(), "result.txt")))
                {
                    var result = sr.ReadLine().Trim();
                    picResult.Image = new Bitmap(Path.Combine(GetCurrentExeDirectoryPath(), result.Replace("/", "")+ ".jpg"));
                }
            }
            catch (Exception exp)
            {
                System.Windows.Forms.MessageBox.Show(exp.Message);
            }
        }
    }
}
