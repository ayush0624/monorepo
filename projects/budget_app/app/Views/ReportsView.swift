import SwiftUI

struct ReportsView: View {
    @ObservedObject var dataStore: DataStore

    var body: some View {
        VStack {
            Text("Reports")
                .font(.largeTitle)
            // Placeholder for reports
            Text("Report charts will go here.")
                .padding()
        }
        .padding()
    }
} 