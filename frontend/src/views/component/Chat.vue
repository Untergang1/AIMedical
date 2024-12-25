<template>
    <div class="chat-interface">
      <div class="chat-window" ref="chatwnd">
        <div class="message-container" ref="messageContainer">
          <div 
            v-for="(message, index) in messages" 
            :key="index" 
            class="message" 
            :class="message.sender">
              <div class="avatar">
                <img :src="getAvatar(message)"/>
              </div>
              <div class="message-content">
                <p>{{ message.text }}</p>
              </div>

            
          </div>
        </div>
      </div>
          <!-- Message Input Section -->
      <div ref='chatInput' class="message-input">
        <input
          v-model="inputMessage" 
          @keyup.enter="sendMessage"
          :placeholder="placeholderText"
          autofocus
          :disabled="isWaitingForBotReply"
        />
<!-- 
        <button 
        :class="{ 'uploaded': uploadedImage, 'default': !uploadedImage }" 
        @click="triggerUpload"
        :disabled="isWaitingForBotReply"
      >
        {{ uploadedImage ? 'Change' : 'Upload' }}
      </button> -->
      <!-- <input 
        type="file" 
        ref="fileInput" 
        @change="handleFileUpload" 
        style="display: none;" 
        accept="image/*" 
      /> -->
      </div>
    </div>
  </template>
  
  <script>
  import { nextTick } from "vue";
  import { mapGetters } from 'vuex'
  import { sendChat } from '@/api/user';


  export default {
    name: 'Chat',
    props: {
      src: ''
    },
    data() {
      return {
        messages: [
          { text: `您好，${this.$store.state.user.realname}！我是您的AI医生，很高兴为您提供健康咨询。请告诉我您目前的症状或健康问题，我会尽力为您提供建议和帮助。`, sender: 'bot' },
        ],
        inputMessage: '',
        isWaitingForBotReply: false, // 用于禁用输入框
      };
    },
    methods: {
      sendMessage() {
        if (this.inputMessage.trim()) {
          this.placeholderText = '等待机器人回复...';
          this.isWaitingForBotReply = true;
          this.messages.push({
            text: this.inputMessage,
            sender: 'user', // Change this based on your logic
          });
          this.inputMessage = ''; // Clear the input after sending
          this.scrollToBottom()

          this.sendMsg()
        }
      },
      getAvatar(message) {
        if(message.sender == 'bot') {
          return 'https://static.vecteezy.com/system/resources/previews/015/412/022/non_2x/doctor-round-avatar-medicine-flat-avatar-with-male-doctor-medical-clinic-team-round-icon-medical-collection-illustration-vector.jpg'
        } else {
          return this.avatar
        }
      },
      scrollToBottom() {
        this.$nextTick(() => {
        const messagesWindow = this.$refs.chatwnd;
        messagesWindow.scrollTop = messagesWindow.scrollHeight;
      });
      },
      sendMsg(){
        const data = {
          messages: this.messages,
          src: this.src,
          username: this.$store.state.user.name
        }
        
        sendChat(data).then((res => {
          this.receiveChat(res)
        }))
      },
      receiveChat(response) {
        try {
          if (response.code === 20000) {
            this.messages.push({
              sender: 'bot',
              text: response.text,
            });
            this.isWaitingForBotReply = false;
          } else {
            this.isWaitingForBotReply = false;
            Message.error('接收失败');
          }
        } catch (error) {
          this.isWaitingForBotReply = false;
          Message.error('处理消息时出错');
          console.error(error);
        } finally {
          this.scrollToBottom()
          this.placeholderText = '提出你的问题'
          this.$refs.chatInput.focus(); // Focus the input box here
        }
      },

      generateBotReply() {
        console.log(this.realname)
        // 生成机器人的回复内容
        const botResponses = [
          '我收到您的消息了，感谢您与我交流！',
          '请稍等，我正在处理您的问题。',
          '这是一个自动回复消息示例。',
          '很高兴能够帮助您！还有其他问题吗？',
        ];
        const randomReply =
          botResponses[Math.floor(Math.random() * botResponses.length)];

        this.messages.push({
          text: randomReply,
          sender: 'bot',
        });
      },
    },
    computed: {
    ...mapGetters([
      'realname',
      'avatar',
      'name',
      'age',
      'height'
    ])
    }
  }

  </script>
  
  <style scoped>

  .chat-interface {
    display: flex;
    flex-direction: column;

    background-color: #f5f5f5;
  }
  
  .chat-window {
    flex: 1;
    width: 100%;
    overflow-y: auto;  /* 仅在消息窗口内部启用垂直滚动条 */
    padding: 10px;
    max-height: 650px;
    background-color: white;
    box-sizing: border-box;
  }
  
  .message-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  
  
  .message {
    display: flex;
    align-items: flex-start;
    padding: 12px;
    max-width: 100%;
  }
  
  .message.user {
    align-self: flex-end; /* 让消息整体靠右 */
    display: flex;        /* 确保子元素可以灵活布局 */
    justify-content: flex-end; /* 子元素内容靠右 */
    margin-left: auto;    /* 防止向左扩展 */
   
  }
  
  .message.assistant {
    align-self: flex-start;
  }
  
  .message .avatar {
    width: 40px;
    height: 40px;
    margin-right: 10px;
  }
  
  .message .avatar img {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
  }
  
  .message .message-content {
    flex-grow: 3;
    display: flex;
    flex-direction: column;
    word-wrap: break-word;

    padding: 3px 20px; /* 添加上下和左右的内边距 */
    max-width: 700px;
    border-radius: 8px;
    overflow: hidden;
  }
  
  .message.user .message-content {
    background-color: #d1e7ff;
  }
  
  .message.assistant .message-content {
    background-color: #f1f1f1;
  }
  
  .message-input {
    height: 100px;
    background-color: white;
    padding: 20px;
    display: flex;
    justify-content: center;
    position: fixed; /* 固定位置 */
    bottom: 0; /* 距离底部 0 */
    width: 80%; /* 占满整个宽度 */
  }
  
  .message-input input {
    margin-left: 10px;
    margin-right: 10px;
    width: 80%;
    height: 60px;
    padding: 10px;
    border-radius: 20px;
    font-size: 16px;
    border: none;
    resize: none;
    background-color: #f5f5f5;
  }
  
  .message-input input:focus {
    outline: none;
    background-color: #e0e0e0;
  }

  .message-input input:disabled {
    background-color: #e0e0e0;
    color: #a0a0a0;
    cursor: not-allowed;
  }
  
  
  
  </style>
  