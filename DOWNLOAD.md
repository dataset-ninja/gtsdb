Dataset **GTSDB** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogImZzOi8vYXNzZXRzLzI2MDFfR1RTREIvZ3RzZGItRGF0YXNldE5pbmphLnRhciIsICJzaWciOiAiaWZyZmtQQVV1ZU1hZWk5aHhuRG9DRGFRVlFVSGlCN0xGeUdIMnAzaGNWTT0ifQ==)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='GTSDB', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be downloaded here:

- [FullIJCNN2013.zip](https://sid.erda.dk/public/archives/ff17dc924eba88d5d01a807357d6614c/FullIJCNN2013.zip)
- [TestIJCNN2013.zip](https://sid.erda.dk/public/archives/ff17dc924eba88d5d01a807357d6614c/TestIJCNN2013.zip)
- [TrainIJCNN2013.zip](https://sid.erda.dk/public/archives/ff17dc924eba88d5d01a807357d6614c/TrainIJCNN2013.zip)
- [gt.txt](https://sid.erda.dk/public/archives/ff17dc924eba88d5d01a807357d6614c/gt.txt)
