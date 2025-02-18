{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyPDJ+bDc00gFWXS9h2JfhGm",
      "include_colab_link": false
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/Syedaashnaghazanfar/Basit-python-game/blob/main/app.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "%%writefile app.py\n",
        "import streamlit as st\n",
        "import pandas as pd\n",
        "import os\n",
        "from io import BytesIO\n",
        "\n",
        "st.set_page_config(page_title=\"💿Data sweeper\", layout=\"wide\")\n",
        "st.title(\"💿Data sweeper\")\n",
        "st.write(\"Transform your CSV and Excel File formats\")\n",
        "\n",
        "# Allow multiple file uploads\n",
        "uploaded_files = st.file_uploader(\"Upload files (CSV or Excel):\", type=[\"csv\", \"xlsx\"], accept_multiple_files=True)\n",
        "\n",
        "if uploaded_files:  # Check if files are uploaded\n",
        "    for file in uploaded_files:\n",
        "        file_name = file.name\n",
        "        file_ext = os.path.splitext(file_name)[-1].lower()\n",
        "\n",
        "        # Read the file\n",
        "        try:\n",
        "            if file_ext == \".csv\":\n",
        "                df = pd.read_csv(file)\n",
        "            elif file_ext == \".xlsx\":\n",
        "                df = pd.read_excel(file, engine='openpyxl')  # Use openpyxl for XLSX\n",
        "            else:\n",
        "                st.error(f\"Unsupported file type: {file_ext}\")\n",
        "                continue\n",
        "\n",
        "            # Display file information\n",
        "            st.write(f\"*File Name:* {file_name}\")\n",
        "            st.write(f\"*File Size:* {file.size / 1024:.2f} KB\")\n",
        "            st.write(f\"*File Type:* {file_ext}\")\n",
        "\n",
        "            # Display first few rows\n",
        "            st.write(\"### Preview of the Data\")\n",
        "            st.dataframe(df.head())\n",
        "\n",
        "            # Data Cleaning Options\n",
        "            st.subheader(\"🔨 Data Cleaning Options\")\n",
        "\n",
        "            if st.checkbox(f\"Clean Data for {file_name}\"):\n",
        "                col1, col2 = st.columns(2)\n",
        "\n",
        "                with col1:\n",
        "                    if st.button(f\"Remove Duplicates from {file_name}\"):\n",
        "                        df.drop_duplicates(inplace=True)\n",
        "                        st.success(f\"Duplicates removed from {file_name}\")\n",
        "\n",
        "                with col2:\n",
        "                    if st.button(f\"Fill Missing Values for {file_name}\"):\n",
        "                        numeric_cols = df.select_dtypes(include=['number']).columns\n",
        "                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())\n",
        "                        st.success(f\"Missing values filled for {file_name}\")\n",
        "\n",
        "            # Select Columns to Convert\n",
        "            st.subheader(\"🛠 Select Columns to Convert\")\n",
        "            columns = st.multiselect(f\"Select columns to convert for {file_name}\", df.columns, default=df.columns)\n",
        "            df = df[columns]\n",
        "\n",
        "            # Data Visualization\n",
        "            st.subheader(\"📊 Data Visualization\")\n",
        "            if st.checkbox(f\"Show Data Visualization for {file_name}\"):\n",
        "                st.bar_chart(df.select_dtypes(include=['number']).iloc[:, :2])\n",
        "\n",
        "            # File Conversion Options\n",
        "            st.subheader(\"📁 Conversion Options\")\n",
        "            conversion_type = st.radio(f\"Convert {file_name} to:\", [\"CSV\", \"Excel\"], key=file.name)\n",
        "\n",
        "            if st.button(f\"Convert {file_name} to {conversion_type}\"):\n",
        "                buffer = BytesIO()\n",
        "                if conversion_type == \"CSV\":\n",
        "                    df.to_csv(buffer, index=False)\n",
        "                    new_file_name = file_name.replace(file_ext, \".csv\")\n",
        "                    mime_type = \"text/csv\"\n",
        "                elif conversion_type == \"Excel\":\n",
        "                    df.to_excel(buffer, index=False, engine='openpyxl')\n",
        "                    new_file_name = file_name.replace(file_ext, \".xlsx\")\n",
        "                    mime_type = \"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet\"\n",
        "\n",
        "                buffer.seek(0)\n",
        "\n",
        "                # Download Button\n",
        "                st.download_button(\n",
        "                    label=f\"⬇ Download {new_file_name}\",\n",
        "                    data=buffer,\n",
        "                    file_name=new_file_name,\n",
        "                    mime=mime_type\n",
        "                )\n",
        "\n",
        "        except Exception as e:\n",
        "            st.error(f\"Error processing {file_name}: {e}\")\n",
        "\n",
        "st.success(\"🎉 All files processed successfully!\")"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "3cVOluc-IMfm",
        "outputId": "79c348aa-7426-406a-af04-fb2fdc5e1d13"
      },
      "execution_count": 13,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Overwriting app.py\n"
          ]
        }
      ]
    }
  ]
}
