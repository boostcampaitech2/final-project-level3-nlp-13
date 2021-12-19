import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import BCEWithLogitsLoss, CrossEntropyLoss, MSELoss

from transformers.models.electra import ElectraPreTrainedModel, ElectraModel
from transformers.modeling_outputs import SequenceClassifierOutput

class ConvHead(nn.Module):

    def __init__(self, config):
        super().__init__()
        self.conv1d_1 = nn.Conv1d(config.hidden_size, config.hidden_size, 1)
        self.conv1d_3 = nn.Conv1d(config.hidden_size, config.hidden_size, 3, padding=1)
        self.conv1d_5 = nn.Conv1d(config.hidden_size, config.hidden_size, 5, padding=2)
        self.drop_out = nn.Dropout(0.7)
        self.fc = nn.Linear(config.hidden_size * 3, config.num_labels , bias=True)

    def forward(self, features : torch.Tensor, **kwargs):
        x = features.transpose(1, 2)
        
        c1, c3, c5 = self.conv1d_1(x), self.conv1d_3(x), self.conv1d_5(x)
        c1, c3, c5 = F.max_pool1d(c1, c1.shape[-1]), F.max_pool1d(c3, c3.shape[-1]), F.max_pool1d(c5, c5.shape[-1])
        c1, c3, c5 = F.relu(c1), F.relu(c3) , F.relu(c5)

        conv_concat = torch.concat([c1, c3, c5], dim=1).squeeze(-1)
        conv_output = self.drop_out(conv_concat)
        conv_output = self.fc(conv_output)

        return conv_output

class CustomForSequenceClassification(ElectraPreTrainedModel):
    def __init__(self, config):
        super().__init__(config)
        self.num_labels = config.num_labels
        self.config = config
        self.electra = ElectraModel(config)
        self.classifier = ConvHead(config)

        # Initialize weights and apply final processing
        self.post_init()

    def forward(
        self,
        input_ids=None,
        attention_mask=None,
        token_type_ids=None,
        position_ids=None,
        head_mask=None,
        inputs_embeds=None,
        labels=None,
        output_attentions=None,
        output_hidden_states=None,
        return_dict=None,
    ):
        r"""
        labels (:obj:`torch.LongTensor` of shape :obj:`(batch_size,)`, `optional`):
            Labels for computing the sequence classification/regression loss. Indices should be in :obj:`[0, ...,
            config.num_labels - 1]`. If :obj:`config.num_labels == 1` a regression loss is computed (Mean-Square loss),
            If :obj:`config.num_labels > 1` a classification loss is computed (Cross-Entropy).
        """
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        discriminator_hidden_states = self.electra(
            input_ids,
            attention_mask,
            token_type_ids,
            position_ids,
            head_mask,
            inputs_embeds,
            output_attentions,
            output_hidden_states,
            return_dict,
        )

        sequence_output = discriminator_hidden_states[0]
        logits = self.classifier(sequence_output)

        loss = None
        if labels is not None:
            if self.config.problem_type is None:
                if self.num_labels == 1:
                    self.config.problem_type = "regression"
                elif self.num_labels > 1 and (labels.dtype == torch.long or labels.dtype == torch.int):
                    self.config.problem_type = "single_label_classification"
                else:
                    self.config.problem_type = "multi_label_classification"

            if self.config.problem_type == "regression":
                loss_fct = MSELoss()
                if self.num_labels == 1:
                    loss = loss_fct(logits.squeeze(), labels.squeeze())
                else:
                    loss = loss_fct(logits, labels)
            elif self.config.problem_type == "single_label_classification":
                loss_fct = CrossEntropyLoss()
                loss = loss_fct(logits.view(-1, self.num_labels), labels.view(-1))
            elif self.config.problem_type == "multi_label_classification":
                loss_fct = BCEWithLogitsLoss()
                loss = loss_fct(logits, labels)

        if not return_dict:
            output = (logits,) + discriminator_hidden_states[1:]
            return ((loss,) + output) if loss is not None else output

        return SequenceClassifierOutput(
            loss=loss,
            logits=logits,
            hidden_states=discriminator_hidden_states.hidden_states,
            attentions=discriminator_hidden_states.attentions,
        )






