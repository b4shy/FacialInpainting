"""
Implement all the losses needed for the Inpainting.
"""
import torch


class Loss():
    def __init__(self, vgg16_model):
        """
        Inits the Loss with the VGG Partial Model
        :param vgg16_model: The VGG Model, which outputs the three MaxPool matrices
        """
        self.vgg16_model = vgg16_model
        self.vgg16_gt_out = None
        self.vgg16_pred_out = None
        self.vgg16_comp_out = None

        self.prediction = None
        self.orig_image_permuted = None
        self.mask_permuted = None

    def prepare_loss_calculation(self, prediction, orig_image, mask):
        """
        Sets the instance variables for the corresponding step and performs the forward pass of the VGG Network
        :param prediction: Output of the PConv Unet
        :param orig_image: Ground Truth
        :param mask: Overlaid Mask
        """
        self.prediction = prediction
        self.orig_image_permuted = orig_image.permute(0, 3, 1, 2).float()
        self.mask_permuted = mask.permute(0, 3, 1, 2).float()

        self.vgg_output()

    def calculate_loss_hole(self):
        """
        L hole loss according to the paper
        :returns: The L Hole Loss
        """

        pp_gt = (1 - self.mask_permuted) * self.orig_image_permuted
        pp_pred = (1 - self.mask_permuted) * self.prediction
        return torch.nn.L1Loss()(pp_gt, pp_pred)

    def calculate_loss_valid(self):
        """
        L valid loss according to the paper
        :returns: The L Hole Loss
        """
        pp_gt = self.mask_permuted * self.orig_image_permuted
        pp_pred = self.mask_permuted * self.prediction
        return torch.nn.L1Loss()(pp_gt, pp_pred)

    def vgg_output(self):
        """
        Calculates the VGG Output on the corresponding instance variables and stores them as instance variable
        """
        self.vgg16_gt_out = self.vgg16_model(self.orig_image_permuted)
        torch.cuda.empty_cache()

        self.vgg16_pred_out = self.vgg16_model(self.prediction)
        torch.cuda.empty_cache()

        comp = self.mask_permuted * self.orig_image_permuted + (1 - self.mask_permuted) * self.prediction
        torch.cuda.empty_cache()

        self.vgg16_comp_out = self.vgg16_model(comp)
        torch.cuda.empty_cache()

    def calculate_perceptual_loss(self):
        """
        Calculates the perceptual Loss
        :returns: Perceptual Loss
        """
        loss = 0
        for pred, gt, cmp in zip(self.vgg16_pred_out, self.vgg16_gt_out, self.vgg16_comp_out):
            loss += (torch.nn.L1Loss()(pred, gt) + torch.nn.L1Loss()(cmp, gt))

        return loss

    def calculate_style_out_loss(self):
        """
        Calculates the Style out Loss
        :returns: Style OutLoss
        """
        loss = 0
        for pred, gt in zip(self.vgg16_pred_out, self.vgg16_gt_out):
            loss += torch.nn.L1Loss()(self.gram_matrix(pred), self.gram_matrix(gt))
        return loss

    def calculate_style_comp_loss(self):
        """
        Calculates the Style Comp Loss
        :returns: Style Comp Loss
        """
        loss = 0
        for pred, gt in zip(self.vgg16_comp_out, self.vgg16_gt_out):
            loss += torch.nn.L1Loss()(self.gram_matrix(pred), self.gram_matrix(gt))
        return loss

    @staticmethod
    def gram_matrix(output):
        """
        Calculates the Gram Matrix on the VGG Output
        :param: Output of the Network
        :returns: Gram Matrix
        """
        (b, ch, h, w) = output.size()
        features = output.view(b, ch, w * h)
        features_t = features.transpose(1, 2)
        gram = features.bmm(features_t) / (ch * h * w)
        return gram


def l_perceptual(vgg16_model, prediction, image, mask, device):
    image_permuted = image.permute(0, 3, 1, 2).float().to(device)
    mask_permuted = mask.permute(0, 3, 1, 2).to(device)
    pred = prediction.to(device)
    vgg16_gt_out = vgg16_model(image_permuted)
    torch.cuda.empty_cache()

    vgg16_pred_out = vgg16_model(pred)
    torch.cuda.empty_cache()

    comp = mask_permuted * image_permuted + (1-mask_permuted)*pred
    torch.cuda.empty_cache()

    vgg16_comp_out = vgg16_model(comp)
    torch.cuda.empty_cache()

    loss = 0
    for pred, gt, cmp in zip(vgg16_pred_out, vgg16_gt_out, vgg16_comp_out):
        loss += (torch.nn.L1Loss()(pred, gt) + torch.nn.L1Loss()(cmp, gt))

    return loss
