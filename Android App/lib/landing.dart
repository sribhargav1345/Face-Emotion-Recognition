import 'package:flutter/material.dart';
import 'package:live_emotion_detection/home_front.dart';
import 'package:live_emotion_detection/main.dart';

import 'home.dart';

void main() {
  runApp(const MyApp());
}

class Landing extends StatelessWidget {
  const Landing({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        centerTitle: true,
        title: const Text('Live Emotion Detection App 🐇'),
        backgroundColor: const Color(0xfffe9400),
      ),
      body: Container(
        padding: const EdgeInsets.fromLTRB(30.0, 15.0, 30.0, 5.0),
        child: SafeArea(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: const [
                  Text(
                    'Major Project',
                    style: TextStyle(fontSize: 25.0, fontWeight: FontWeight.bold),
                  ),
                ],
              ),
              const SizedBox(height: 5.0),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: const [
                  Text(
                    'Face Emotion Recognition - CSD Project',
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                    ),
                  )
                ],
              ),
              const SizedBox(height: 30.0),
              const Text(
                'Choose from the following options -',
                style: TextStyle(fontSize: 15),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 15.0),
              _buildButton(
                context,
                'Using Back Camera',
                () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => const Home()),
                  );
                },
              ),
              const SizedBox(height: 15.0),
              _buildButton(
                context,
                'Using Front Camera',
                () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => const HomeFront()),
                  );
                },
              ),
              const SizedBox(height: 15.0),
              const Text('Made with ❤ Group-21', textAlign: TextAlign.center),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildButton(BuildContext context, String text, VoidCallback onPressed) {
    return Container(
      margin: const EdgeInsets.symmetric(vertical: 5.0),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [
            Color(0xFF0D47A1),
            Color(0xFF1976D2),
            Color(0xFF42A5F5),
          ],
        ),
        borderRadius: BorderRadius.circular(4),
      ),
      child: TextButton(
        style: TextButton.styleFrom(
          primary: Colors.white,
          padding: const EdgeInsets.symmetric(vertical: 45.0, horizontal: 30.0),
          textStyle: const TextStyle(fontSize: 20),
        ),
        onPressed: onPressed,
        child: Center(
          child: Text(
            text,
            textAlign: TextAlign.center,
          ),
        ),
      ),
    );
  }
}
