import { AfterViewChecked, Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';



@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent implements OnInit, AfterViewChecked {
  title = 'VCABuddy_ui';
  @ViewChild('chatContainer') chatContainer!: ElementRef;
  recognition: any;
  isRecording = false;
  recordedText = '';
  textInputContent = '';
  chatResponses$!: Observable<Chat[]>;
  backendUrl = 'http://127.0.0.1:8000/media/';
  isLoading: boolean = false;
  selectedLanguage = 'Select Language'
  keywordActionsTwi = new Map<string, string>([
    ['data', 'mɛyɛ dɛn atɔ mtn data'],
    ['office', 'ɛhe na metumi ahwehwɛ mtn office'],
    ['hello', 'hello'],
    ['internet', 'Me ntumi nnya intanɛt nkitahodi mfiri me sim card so'],
  ]);
  keywordActionsEwe = new Map<string, string>([
    ['data', 'aleke mawɔ aƒle mtn data bundle'],
    ['office', 'afi kae mate ŋu akpɔ mtn ɔfis le'],
    ['internet', 'Nyemete ŋu xɔ internet kadodo tso nye sim card dzi o'],
    ['hello', 'hello'],
  ]);


  constructor(private httpClient: HttpClient) {
    this.chatContainer = new ElementRef(null);
    this.recognition = new (window as any).webkitSpeechRecognition();
    this.recognition.lang = 'ee';
    this.recognition.continuous = false;
    this.recognition.interimResults = true;

  }
  ngAfterViewChecked(): void {

  }
  ngOnInit(): void {
    this.getAllChats()
  }

  toggleRecording() {
    // Toggle the recording state
    this.isRecording = !this.isRecording;

    if (this.isRecording) {
      // Start recording logic here
      this.startRecording();
    } else {
      // Stop recording logic here
      this.stopRecording();
    }
  }

  sendTextChat() {
    this.isLoading = true;
    this.recordedText = this.textInputContent
    this.sendMessage('text')
  }

  startRecording() {
    this.isRecording = true;
    this.recordedText = '';
    this.recognition.start();
  }
  stopRecording() {
    this.isLoading = true;
    this.recognition.stop();
    this.isRecording = false;
    this.recognition.onresult = (event: any) => {
      const result = event.results[event.results.length - 1];
      if (result.isFinal) {
        this.recordedText = result[0].transcript;
        if (this.selectedLanguage == 'Twi') {
          const matchingAction = this.findKeywordInText(this.recordedText, this.keywordActionsTwi);

          if (matchingAction !== undefined) {
            console.log(`Matching action: ${matchingAction}`);
            this.recordedText = matchingAction;
          } else {
            alert("We do not support this input yet")
          }

        }
        else if (this.selectedLanguage == 'Ewe') {
          const matchingAction = this.findKeywordInText(this.recordedText, this.keywordActionsEwe);

          if (matchingAction !== undefined) {
            console.log(`Matching action: ${matchingAction}`);
            this.recordedText = matchingAction;
          } else {
            alert("We do not support this input yet")
          }
        }
        this.isRecording = false;
        this.sendMessage('voice');
      }
    };
  }

  sendMessage(input_type: string) {

    const textMessage = this.recordedText;
    this.httpClient.post('http://127.0.0.1:8000/chat/api/chat_messages/', { message: textMessage, input_type: input_type, language: this.selectedLanguage })
      .subscribe((response) => {
        this.textInputContent = "";
        this.getAllChats();
        this.isLoading = false;
      }, (error) => {
        // Handle error here
        console.error('Error:', error);
        this.isLoading = false;
      });
  }

  getAllChats() {
    this.chatResponses$ = this.httpClient.get<Chat[]>('http://127.0.0.1:8000/chat/api/chat_messages/');
    this.isLoading = false;
    this.chatResponses$.subscribe(() => {
      // Scroll to the bottom only when new data arrives
    });
  }

  processAudioUrl(audioFileName: string): string {
    // Concatenate the backend URL and the audio file name
    return `${this.backendUrl}${audioFileName}`;
  }

  findKeywordInText(text: string, keywordActions: any): string | undefined {
    for (const [keyword, action] of keywordActions) {
      if (text.includes(keyword)) {
        return action;
      }
    }
    return undefined; // Return undefined if no keyword is found
  }
}


export interface Chat {
  id: number,
  user_id: number,
  message: string,
  response: string,
  timestamp: string
}
