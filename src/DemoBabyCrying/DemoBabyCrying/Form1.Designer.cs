namespace DemoBabyCrying
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.startRecordBtn = new System.Windows.Forms.Button();
            this.endRecordBtn = new System.Windows.Forms.Button();
            this.picResult = new System.Windows.Forms.PictureBox();
            ((System.ComponentModel.ISupportInitialize)(this.picResult)).BeginInit();
            this.SuspendLayout();
            // 
            // startRecordBtn
            // 
            this.startRecordBtn.Font = new System.Drawing.Font("Microsoft Sans Serif", 13.8F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.startRecordBtn.Location = new System.Drawing.Point(148, 37);
            this.startRecordBtn.Margin = new System.Windows.Forms.Padding(4);
            this.startRecordBtn.Name = "startRecordBtn";
            this.startRecordBtn.Size = new System.Drawing.Size(302, 134);
            this.startRecordBtn.TabIndex = 0;
            this.startRecordBtn.Text = "Start Record";
            this.startRecordBtn.UseVisualStyleBackColor = true;
            this.startRecordBtn.Click += new System.EventHandler(this.startRecordBtn_Click);
            // 
            // endRecordBtn
            // 
            this.endRecordBtn.Font = new System.Drawing.Font("Microsoft Sans Serif", 13.8F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.endRecordBtn.Location = new System.Drawing.Point(594, 37);
            this.endRecordBtn.Margin = new System.Windows.Forms.Padding(4);
            this.endRecordBtn.Name = "endRecordBtn";
            this.endRecordBtn.Size = new System.Drawing.Size(309, 134);
            this.endRecordBtn.TabIndex = 1;
            this.endRecordBtn.Text = "End Record";
            this.endRecordBtn.UseVisualStyleBackColor = true;
            this.endRecordBtn.Click += new System.EventHandler(this.endRecordBtn_Click);
            // 
            // picResult
            // 
            this.picResult.Location = new System.Drawing.Point(152, 202);
            this.picResult.Name = "picResult";
            this.picResult.Size = new System.Drawing.Size(751, 371);
            this.picResult.TabIndex = 2;
            this.picResult.TabStop = false;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1082, 617);
            this.Controls.Add(this.picResult);
            this.Controls.Add(this.endRecordBtn);
            this.Controls.Add(this.startRecordBtn);
            this.Margin = new System.Windows.Forms.Padding(4);
            this.Name = "Form1";
            this.Text = "Smart Baby Crying";
            ((System.ComponentModel.ISupportInitialize)(this.picResult)).EndInit();
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Button startRecordBtn;
        private System.Windows.Forms.Button endRecordBtn;
        private System.Windows.Forms.PictureBox picResult;
    }
}

