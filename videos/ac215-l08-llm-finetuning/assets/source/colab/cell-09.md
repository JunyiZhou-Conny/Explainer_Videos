## <font color ='#16AD04'>**4. Hugging Face Access Token** </font>

To download models and datasets from Hugging Face Hub, you will need to create a free account and generate an access token. Follow these steps:

1.  **Sign up on Hugging Face:**
    *   Go to [huggingface.co/join](https://huggingface.co/join).
    *   Choose a sign-up method (email, Google, GitHub).
    *   Fill in the required information and create your account.

2.  **Create an Access Token:**
    *   Once logged in, click on your profile picture in the top right corner.
    *   Select **Settings**.
    *   In the left-hand menu, click on **Access Tokens**.
    *   Click on **New token**.
    *   Give your token a name (e.g., `hf-colab-token`).
    *   Choose a role (Read is enough for Steps 1-6.2; the optional upload in Step 6.3 needs write).
    *   Click **Generate token**.
    *   **Copy the generated token immediately.** You will not be able to see it again after leaving the page.

3.  **Add the Access Token to Colab Secrets:**
    *   In your Google Colab notebook, click on the **🔑 (Secrets)** icon in the left sidebar.
    *   Click on **+ New secret**.
    *   In the **Name** field, enter `HF_TOKEN`.
    *   In the **Value** field, paste the access token you copied from Hugging Face.
    *   Ensure the **Notebook access** toggle is turned **ON**.

Now you can access your Hugging Face token in your Colab notebook using the following code: