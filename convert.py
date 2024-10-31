import os
import shutil
import xml.etree.ElementTree as ET

def copy_files(source_path, filenames):
    for filename in filenames:
        if filename.endswith(".xml"):
            shutil.copy(os.path.join(source_path, filename), annotations_path)
        elif filename.endswith(".jpg"):
            shutil.copy(os.path.join(source_path, filename), images_path)

def save_to_txt(file_list, file_path):
    with open(file_path, "w") as f:
        for item in file_list:
            f.write(f"{item}\n")

# Paths to the original dataset
original_dataset_path = "data/OverdimensionVihacle.v5i.voc"
train_path = os.path.join(original_dataset_path, "train")
test_path = os.path.join(original_dataset_path, "test")
valid_path = os.path.join(original_dataset_path, "valid")

# New paths for VOC format
voc_path = "data/OverdimensionVihacle.v5i.voc.jetson"
annotations_path = os.path.join(voc_path, "Annotations")
images_path = os.path.join(voc_path, "JPEGImages")
image_sets_path = os.path.join(voc_path, "ImageSets", "Main")

os.makedirs(annotations_path, exist_ok=True)
os.makedirs(images_path, exist_ok=True)
os.makedirs(image_sets_path, exist_ok=True)

# Copy train files
train_files = [os.path.splitext(f)[0] for f in os.listdir(train_path) if f.endswith('.xml')]
copy_files(train_path, os.listdir(train_path))

# Copy test files
test_files = [os.path.splitext(f)[0] for f in os.listdir(test_path) if f.endswith('.xml')]
copy_files(test_path, os.listdir(test_path))

# Copy validation files
valid_files = [os.path.splitext(f)[0] for f in os.listdir(valid_path) if f.endswith('.xml')]
copy_files(valid_path, os.listdir(valid_path))

# Save the file lists
save_to_txt(train_files, os.path.join(image_sets_path, "train.txt"))
save_to_txt(test_files, os.path.join(image_sets_path, "test.txt"))
save_to_txt(valid_files, os.path.join(image_sets_path, "val.txt"))
save_to_txt(train_files + valid_files, os.path.join(image_sets_path, "trainval.txt"))

# Extract labels from XML files
label_set = set()
for xml_file in os.listdir(annotations_path):
    if xml_file.endswith(".xml"):
        tree = ET.parse(os.path.join(annotations_path, xml_file))
        root = tree.getroot()
        for obj in root.findall("object"):
            label_name = obj.find("name").text
            label_set.add(label_name)

# Save labels to labels.txt
with open(os.path.join(voc_path, "labels.txt"), "w") as f:
    for label in sorted(label_set):
        f.write(f"{label}\n")

print("Dataset conversion to Jetson VOC format is completed.")