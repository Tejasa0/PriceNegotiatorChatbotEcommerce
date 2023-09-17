class Chatbox{
    constructor(){
        this.args={
            openButton: document.querySelector('.chatbox__button button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton : document.querySelector('.send__button'),
        }


        this.state=false;
        this.messages=[];
        this.id=0;
        this.pName="";
        this.price=0;
        this.flag=false;
    }
    initial1(chatBox)
    {
    if(flag1==0){
            this.toggleState(chatBox);
            var html='';
            html= html + '<div class="messages__item messages__item--visitor prod">'+ '<img src="../static/images/Products/'+ this.id + '/'+this.id+'.jpeg" alt="img" />'+'<h6 class="prod-name"> <strong>'+ this.pName +' </strong></h6>'+'<h6 class="price-tag "><strong style="color:blue"><box-icon class="rupee"></box-icon>'+this.price+'</strong></h6>'+'</div>';
            const chatmessage=chatBox.querySelector('.chatbox__messages');
            //chatmessage.innerHTML=html;

            let msg1={name:'Naitro', message:html}
            this.messages.push(msg1);
            console.log(flag1);
            flag1=1;
            }
            //console.log(this.id);
//            let text1=this.id;
//            fetch('/sendId', {
//            method:'POST',
//            body: JSON.stringify({id:text1}),
//            mode:'cors',
//            headers:{
//                'Accept': 'application/json',
//                'Content-Type': 'application/json;charset=utf-8'
//            },
//        });
            this.updateChatText(chatBox);



        }


    display(){

        const{openButton,chatBox,sendButton}=this.args;
        openButton.addEventListener('click',()=>this.toggleState(chatBox));

        openButton.addEventListener('click',()=>this.initial1(chatBox));

        sendButton.addEventListener('click',()=>this.onSendButton(chatBox))


        const node=chatBox.querySelector('input');
        node.addEventListener('keyup',({key})=>{
        if(key==="Enter"){
            this.onSendButton(chatBox)
        }
    })
    }

    toggleState(chatbox){
        this.state=!this.state;



        if(this.state){
            chatbox.classList.add('chatbox--active')

}
       else{
            chatbox.classList.remove('chatbox--active')
        }
    }

    onSendButton(chatbox){

        var textField=chatbox.querySelector('input');

        let text1=textField.value;
        if(text1===""){
            return;
        }

        let msg1={name:'User', message:text1}
        this.messages.push(msg1);
        let id=this.id
        fetch('/predict', {
            method:'POST',
            body: JSON.stringify({
            message: text1,
            id1: id,
            }),
//           body: JSON.stringify({message:text1,id1:id}),
            mode:'cors',
            headers:{
                'Accept': 'application/json',
                'Content-Type': 'application/json;charset=utf-8'
            },
        })



        .then((r)=>r.json())
        .then((r)=>{
            let msg2={name:'Naitro',message:r.answer};
            this.messages.push(msg2);


            this.updateChatText(chatbox)
            textField.value=''
        }).catch((error)=> {
            console.error('Error:',error);





            this.updateChatText(chatbox)
            textField.value=''
        });
    }




    updateChatText(chatbox){
        var html='';

        this.messages.slice().reverse().forEach(function(item){

            if(item.name==='Naitro'){
                html= html + '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
            }

            else{
                html= html + '<div class="messages__item messages__item--operator">' + item.message + '</div>'
            }
        });
        const chatmessage=chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML=html;
    }
}

var flag=0;
var flag1=0;
const chatbox=new Chatbox();

 function show(id,pName,price){
    if(flag==0){
        chatbox.id=id;
        chatbox.pName=pName;
        chatbox.price=price;
        flag=1;
    }
}
chatbox.display();

