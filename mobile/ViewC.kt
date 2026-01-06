package com.example.oulumobilecomputing

import android.net.Uri
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.unit.dp
import androidx.navigation.NavHostController
import androidx.navigation.NavBackStackEntry
import coil.compose.rememberAsyncImagePainter

@OptIn(ExperimentalMaterial3Api::class) // Suppresses the experimental API warning
@Composable
fun ViewC(navController: NavHostController) {
    val backStackEntry: NavBackStackEntry = remember { navController.previousBackStackEntry!! }
    val username = backStackEntry.savedStateHandle.get<String>("username") ?: "Default User"
    val imageUri = backStackEntry.savedStateHandle.get<String>("imageUri")

    Scaffold(
        topBar = {
            TopAppBar(title = { Text("Chat with $username") })
        }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(16.dp)
        ) {
            // Chat Section Title
            Text(
                text = "Conversation",
                style = MaterialTheme.typography.headlineSmall,
                modifier = Modifier.padding(bottom = 16.dp)
            )

            // Chat List
            LazyColumn(
                modifier = Modifier
                    .fillMaxSize()
                    .weight(1f)
            ) {
                items(10) { index ->
                    ChatMessage(
                        isSender = index % 2 == 0,
                        message = if (index % 2 == 0) "Hello! How are you?" else "I'm good, thanks! How about you?",
                        profileUri = imageUri,
                        username = if (index % 2 == 0) username else "You"
                    )
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            // Back Button
            Button(
                onClick = { navController.popBackStack("ViewA", inclusive = false) },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Back to View A")
            }
        }
    }
}

@Composable
fun ChatMessage(isSender: Boolean, message: String, profileUri: String?, username: String) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 8.dp),
        horizontalArrangement = if (isSender) Arrangement.End else Arrangement.Start,
        verticalAlignment = Alignment.Top
    ) {
        // Profile Picture for Receiver (on the left)
        if (!isSender) {
            ProfileIcon(profileUri)
        }

        // Chat Bubble
        Column(
            modifier = Modifier
                .padding(horizontal = 8.dp)
                .widthIn(max = 240.dp)
        ) {
            // Username
            if (!isSender) {
                Text(
                    text = username,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.primary
                )
            }
            Card(
                shape = MaterialTheme.shapes.medium,
                colors = CardDefaults.cardColors(
                    containerColor = if (isSender) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant
                )
            ) {
                Text(
                    text = message,
                    style = MaterialTheme.typography.bodyMedium,
                    color = if (isSender) MaterialTheme.colorScheme.onPrimary else MaterialTheme.colorScheme.onSurface,
                    modifier = Modifier.padding(8.dp)
                )
            }
        }

        // Profile Picture for Sender (on the right)
        if (isSender) {
            ProfileIcon(profileUri)
        }
    }
}

@Composable
fun ProfileIcon(profileUri: String?) {
    Image(
        painter = rememberAsyncImagePainter(Uri.parse(profileUri)),
        contentDescription = "Profile Picture",
        modifier = Modifier
            .size(40.dp) // Icon size
            .padding(4.dp),
        contentScale = ContentScale.Crop
    )
}
