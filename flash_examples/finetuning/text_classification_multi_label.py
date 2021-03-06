# Copyright The PyTorch Lightning team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from torchmetrics import F1

import flash
from flash.core.data.utils import download_data
from flash.text import TextClassificationData, TextClassifier

# 1. Download the data from the Kaggle Toxic Comment Classification Challenge:
# https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge
download_data("https://pl-flash-data.s3.amazonaws.com/jigsaw_toxic_comments.zip", "data/")

# 2. Load the data
datamodule = TextClassificationData.from_csv(
    "comment_text",
    ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"],
    train_file="data/jigsaw_toxic_comments/train.csv",
    test_file="data/jigsaw_toxic_comments/test.csv",
    predict_file="data/jigsaw_toxic_comments/predict.csv",
    batch_size=16,
    val_split=0.1,
    backbone="unitary/toxic-bert",
)

# 3. Build the model
model = TextClassifier(
    num_classes=datamodule.num_classes,
    multi_label=True,
    metrics=F1(num_classes=datamodule.num_classes),
    backbone="unitary/toxic-bert",
)

# 4. Create the trainer
trainer = flash.Trainer(fast_dev_run=True)

# 5. Fine-tune the model
trainer.finetune(model, datamodule=datamodule, strategy="freeze")

# 6. Generate predictions for a few comments!
predictions = model.predict([
    "No, he is an arrogant, self serving, immature idiot. Get it right.",
    "U SUCK HANNAH MONTANA",
    "Would you care to vote? Thx.",
])
print(predictions)

# 7. Save it!
trainer.save_checkpoint("text_classification_multi_label_model.pt")
