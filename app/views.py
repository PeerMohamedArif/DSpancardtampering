from app import app
from flask import request,render_template
import os
from PIL import Image
from skimage.metrics import structural_similarity
import imutils
import cv2
import mysql.connector
from app import app, get_db_connection


app.config['INITIAL_FILE_UPLOADS'] = 'app/static/uploads'
app.config['EXISTNG_FILE'] = 'app/static/original'
app.config['GENERATED_FILE']='app/static/generated'

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    
    if request.method == "POST":
        file_upload=request.files['file_upload']
        filename=file_upload.filename

        # Resize and save the uploaded image
        uploaded_image = Image.open(file_upload).resize((250,160))
        uploaded_image.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'image.jpg'))


        # Resize and save the original image to ensure both uploaded and original matches in size
        original_image = Image.open(os.path.join(app.config['EXISTNG_FILE'], 'image.jpg')).resize((250,160))
        original_image.save(os.path.join(app.config['EXISTNG_FILE'], 'image.jpg'))

        # Read uploaded and original image as array
        original_image = cv2.imread(os.path.join(app.config['EXISTNG_FILE'], 'image.jpg'))
        uploaded_image = cv2.imread(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'image.jpg'))

        # Convert image into grayscale
        original_gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        uploaded_gray = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)

        # Calculate structural similarity
        (score, diff) = structural_similarity(original_gray, uploaded_gray, full=True)
        diff = (diff * 255).astype("uint8")  # based on the image coordinates above to normalise it to 0-255

        # Threshold the differencce and contours between the two images
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(uploaded_image, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # Save all output images (if required)
        # Save original image, uploaded image, difference, and threshold as output images
        cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_original.jpg'), original_image)
        cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_uploaded.jpg'), uploaded_image)
        cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_diff.jpg'), diff)
        cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_thresh.jpg'), thresh)
        
        connection = get_db_connection()
        cursor = connection.cursor()
        query = """
        INSERT INTO comparisons (uploaded_image, original_image, similarity_score)
        VALUES (%s, %s, %s)
        """
        data = ('image.jpg', 'image.jpg', round(score * 100, 2))
        cursor.execute(query, data)
        connection.commit()
        cursor.close()
        connection.close()

        # Return the score (in percentage) as a string, rounded to 2 decimal places
        return render_template('index.html',pred=str(round(score*100,2)) + '%' + ' correct')
    




# Main function
if __name__ == '__main__':
    app.run(debug=True)
    

       






