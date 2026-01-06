package com.example.oulumobilecomputing

import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Button
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavHostController

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ViewA(navController: NavHostController) {
    Scaffold(
        topBar = {
            TopAppBar(title = { Text("View A - Main View") })
        }
    ) { innerPadding ->
        // The Button is placed *above* the scrolling content.
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
        ) {
            // Button at the top to navigate to View B
            Button(
                onClick = { navController.navigate("viewB") },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp)
            ) {
                Text("Go to View B")
            }

            // Your large scrollable content below the button
            MyAppContent(
                modifier = Modifier
                    .weight(1f)  // Fill remaining space
            )
        }
    }
}

@Composable
fun MyAppContent(modifier: Modifier = Modifier) {
    var isClicked by remember { mutableStateOf(false) }
    val scrollState = rememberScrollState()

    Column(
        modifier = modifier
            .verticalScroll(scrollState)
            .padding(16.dp)
    ) {
        // First Image
        Image(
            painter = painterResource(id = R.drawable.my_image), // Replace with your drawable
            contentDescription = "Custom Image",
            modifier = Modifier
                .fillMaxWidth()
                .height(200.dp),
            contentScale = ContentScale.Crop
        )

        Spacer(modifier = Modifier.height(16.dp))

        // Headline Text
        Text(
            text = "Welcome to Jetpack Compose!",
            fontSize = 24.sp,
            fontWeight = FontWeight.Bold
        )

        Spacer(modifier = Modifier.height(8.dp))

        // Secondary Text
        Text(
            text = "This is an example of a secondary text style.",
            fontSize = 16.sp,
            fontWeight = FontWeight.Normal
        )

        Spacer(modifier = Modifier.height(16.dp))

        // Second Image
        Image(
            painter = painterResource(id = R.drawable.my_image_02), // Replace with your drawable
            contentDescription = "Second Image",
            modifier = Modifier
                .fillMaxWidth()
                .height(200.dp),
            contentScale = ContentScale.Crop
        )

        Spacer(modifier = Modifier.height(16.dp))

        // Clickable Button
        Button(onClick = { isClicked = !isClicked }) {
            Text(text = if (isClicked) "Clicked!" else "Click Me")
        }

        // Conditional Content
        if (isClicked) {
            Spacer(modifier = Modifier.height(16.dp))
            Text(
                text = "You clicked the button!",
                fontSize = 18.sp,
                fontWeight = FontWeight.Medium
            )
        }

        // Extra spacer to ensure more scrolling
        Spacer(modifier = Modifier.height(50.dp))

        // Add more lines to force scrolling
        repeat(20) {
            Text(
                text = "Extra content line ${it + 1}",
                fontSize = 16.sp,
                fontWeight = FontWeight.Normal
            )
            Spacer(modifier = Modifier.height(16.dp))
        }
    }
}



