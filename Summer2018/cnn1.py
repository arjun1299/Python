import torch
import fashion_download
import torch.nn as nn
import torchvision.transforms as transforms
from torch.autograd import Variable
train_dataset=fashion_download.fashion(root='./data',train=True,transform=transforms.ToTensor(),download=True)
test_dataset=fashion_download.fashion(root='./data',train=False,transform=transforms.ToTensor(),download=True)
batch_size=100
n_iters=18000
num_epochs=n_iters/(len(train_dataset)/batch_size)
num_epochs=int(num_epochs)
train_loader=torch.utils.data.DataLoader(dataset=train_dataset,batch_size=batch_size,shuffle=True)
test_loader=torch.utils.data.DataLoader(dataset=test_dataset,batch_size=batch_size,shuffle=True)
class CNNModule(nn.Module):
#use elu since it is superior and smoother than relu
    def __init__(self):
        super (CNNModule,self).__init__()

        self.cnn1 = nn.Conv2d(in_channels=1,out_channels=20,kernel_size=5,stride=1,padding=2)
        self.elu1=nn.ELU()
#max pool is superior to average pool
        self.MaxPool1=nn.MaxPool2d(kernel_size=2)

        self.cnn2=nn.Conv2d(in_channels=20,out_channels=40,kernel_size=5,stride=1,padding=2)
        self.elu2=nn.ELU()


        self.MaxPool2=nn.MaxPool2d(kernel_size=2)

        self.fcl=nn.Linear(40*7*7,10)


    def forward(self,x):
        out=self.cnn1(x)
        out=self.elu1(out)

        out=self.MaxPool1(out)

        out=self.cnn2(out)
        out=self.elu2(out)
        out=self.MaxPool2(out)

        out=out.view(out.size(0),-1)

        out=self.fcl(out)

        return out
model=CNNModule()
criterion=nn.CrossEntropyLoss()
learning_rate=0.01
optimizer=torch.optim.SGD(model.parameters(),lr=learning_rate)
iter=0
for epoch in range(num_epochs):
    for i,(images,labels) in enumerate (train_loader):
        images=Variable(images)
        labels=Variable(labels)

        optimizer.zero_grad()
        outputs=model(images)
        loss=criterion(outputs,labels)
        loss.backward()
        optimizer.step()
        iter+=1
        if iter%500==0:
            correct=0
            total=0
            for images,labels in test_loader:
                images=Variable(images)

                outputs=model(images)

                _,predicted=torch.max(outputs.data,1)
                total+=labels.size(0)
                correct+=(predicted==labels).sum()
            accuracy= (100.0* correct)/(total)
            print("Iteration:"+str(iter)+"  Loss:"+str(loss)+"  Accuracy:"+str(accuracy))

#saving trained model
torch.save(torch.save(model.state_dict(),'fashion.pkl'))
