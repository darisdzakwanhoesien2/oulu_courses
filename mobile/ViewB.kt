package com.example.oulumobilecomputing

import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.unit.dp
import androidx.navigation.NavHostController
import coil.compose.rememberAsyncImagePainter

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ViewB(navController: NavHostController) {
    var username by remember { mutableStateOf("") }
    var imageUri by remember { mutableStateOf<Uri?>(null) }

    // Image picker launcher
    val imagePickerLauncher = rememberLauncherForActivityResult(ActivityResultContracts.GetContent()) { uri ->
        imageUri = uri
    }

    Scaffold(
        topBar = {
            TopAppBar(title = { Text("View B") })
        }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(16.dp)
        ) {
            // Title
            Text(
                text = "This is View B",
                style = MaterialTheme.typography.headlineMedium
            )

            Spacer(modifier = Modifier.height(16.dp))

            // Input Field for Username
            Text("Enter Username:")
            OutlinedTextField(
                value = username,
                onValueChange = { username = it },
                modifier = Modifier.fillMaxWidth(),
                label = { Text("Username") }
            )

            Spacer(modifier = Modifier.height(16.dp))

            // Button to Pick Profile Picture
            Button(
                onClick = { imagePickerLauncher.launch("image/*") },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Pick Profile Picture")
            }

            Spacer(modifier = Modifier.height(16.dp))

            // Display Selected Image
            imageUri?.let {
                Image(
                    painter = rememberAsyncImagePainter(it),
                    contentDescription = "Selected Image",
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(200.dp),
                    contentScale = ContentScale.Crop
                )
            }

            Spacer(modifier = Modifier.height(16.dp))

            // Button to Navigate to View C
            Button(
                onClick = {
                    navController.currentBackStackEntry?.savedStateHandle?.apply {
                        set("username", username)
                        set("imageUri", imageUri.toString())
                    }
                    navController.navigate("ViewC")
                },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Go to View C")
            }

            Spacer(modifier = Modifier.height(16.dp))

            // Back to View A
            Button(
                onClick = {
                    navController.navigate("ViewA") {
                        // Remove everything up to "ViewA" from the back stack
                        popUpTo("ViewA") {
                            inclusive = true
                        }
                    }
                },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Back to View A")
            }
        }
    }
}


