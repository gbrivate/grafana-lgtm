import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {ApiService} from './api.service';
import {FormsModule} from '@angular/forms';
import {SignService} from './sign.service';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('fastapi-mfe-test');

  diceResults: any[] = [];
  statusCode: any;
  loop: any;
  content: string = '';
  hash = signal('');
  status= signal('');
  msg= signal('');

  constructor(private api: ApiService, private sign:SignService) {}

  rollDice() {
    this.api.rollDice('gabriel').subscribe(res => {
      this.diceResults.push({
        time: new Date().toISOString(),
        result: res.result
      });
    });
  }

  callSlow() {
    this.api.slow(500).subscribe(res => {
      this.diceResults.push({
        time: new Date().toISOString(),
        result: res.message
      });
    });
  }

  error() {
    this.api.error(this.statusCode).subscribe(res => {

    });
  }

  callLoop() {
    this.api.callLoop(this.loop).subscribe(res => {});
  }

  callJava() {
    this.api.callJava().subscribe(res => {});
  }

  verifyData() {
    console.log(this.hash());
    console.log(this.content);
    this.sign.verifyDocument(this.hash(), this.content).subscribe((res: any) => {
      this.msg.set(res.message);
    },(error) => {
      this.msg.set(error.error.detail)
    })
  }

  signHash() {
    this.sign.signDocument(this.content).subscribe((res: any) => {
      const body= JSON.parse(res);
      this.status.set(body.status);
      this.hash.set(body.signature);
    })
  }

}
