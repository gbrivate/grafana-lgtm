import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {ApiService} from './api.service';
import {FormsModule} from '@angular/forms';

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

  constructor(private api: ApiService) {}

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
}
