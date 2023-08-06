from strhub.models.utils import create_model


dependencies = ['torch', 'pytorch_lightning', 'timm']

class HubConf:

    @staticmethod
    def parseq_tiny(pretrained: bool = False, decode_ar: bool = True, refine_iters: int = 1, **kwargs):
        """
        PARSeq tiny model (img_size=128x32, patch_size=8x4, d_model=192)
        @param pretrained: (bool) Use pretrained weights
        @param decode_ar: (bool) use AR decoding
        @param refine_iters: (int) number of refinement iterations to use
        """
        return create_model('parseq-tiny', pretrained, decode_ar=decode_ar, refine_iters=refine_iters, **kwargs)

    @staticmethod
    def parseq(pretrained: bool = False, decode_ar: bool = True, refine_iters: int = 1, **kwargs):
        """
        PARSeq base model (img_size=128x32, patch_size=8x4, d_model=384)
        @param pretrained: (bool) Use pretrained weights
        @param decode_ar: (bool) use AR decoding
        @param refine_iters: (int) number of refinement iterations to use
        """
        return create_model('parseq', pretrained, decode_ar=decode_ar, refine_iters=refine_iters, **kwargs)

    @staticmethod
    def abinet(pretrained: bool = False, iter_size: int = 3, **kwargs):
        """
        ABINet model (img_size=128x32)
        @param pretrained: (bool) Use pretrained weights
        @param iter_size: (int) number of refinement iterations to use
        """
        return create_model('abinet', pretrained, iter_size=iter_size, **kwargs)

    @staticmethod
    def trba(pretrained: bool = False, **kwargs):
        """
        TRBA model (img_size=128x32)
        @param pretrained: (bool) Use pretrained weights
        """
        return create_model('trba', pretrained, **kwargs)

    @staticmethod
    def vitstr(pretrained: bool = False, **kwargs):
        """
        ViTSTR small model (img_size=128x32, patch_size=8x4, d_model=384)
        @param pretrained: (bool) Use pretrained weights
        """
        return create_model('vitstr', pretrained, **kwargs)

    @staticmethod
    def crnn(pretrained: bool = False, **kwargs):
        """
        CRNN model (img_size=128x32)
        @param pretrained: (bool) Use pretrained weights
        """
        return create_model('crnn', pretrained, **kwargs)

    @staticmethod
    def get_model(model_name):
        return {
            'parseq': HubConf.parseq,
            'parseq_tiny': HubConf.parseq_tiny,
            'abinet': HubConf.abinet,
            'vitstr': HubConf.vitstr,
            'trba': HubConf.trba,
            'crnn': HubConf.crnn,
        }.get(model_name)()
