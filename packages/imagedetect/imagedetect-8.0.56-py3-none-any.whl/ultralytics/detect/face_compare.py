# import face_recognition
#
#
# def face_compare(img1, img2):
#     # 加载图片
#     image1 = face_recognition.load_image_file(img1)
#     image2 = face_recognition.load_image_file(img2)
#
#     # 识别面部特征
#     face1 = face_recognition.face_encodings(image1)[0]
#     face2 = face_recognition.face_encodings(image2)[0]
#
#     # 比较面部特征相似度
#     results = face_recognition.compare_faces([face1], face2)
#
#     # 显示结果
#     if results[0]:
#         print("这两张图片是同一个人")
#     else:
#         print("这两张图片不是同一个人")
#
#
# if __name__ == '__main__':
#     face_compare('image/a.jpeg', 'image/b.jpeg')
#     face_compare('image/c.jpeg', 'image/d.jpeg')
