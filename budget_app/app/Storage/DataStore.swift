import SwiftUI

@MainActor
final class DataStore: ObservableObject {
    @Published private(set) var transactions: [Transaction] = []
    @Published private(set) var categories: [Category] = []
    
    private let fileManager: FileManager
    private let decoder: JSONDecoder
    private let encoder: JSONEncoder
    private let baseURL: URL
    
    init(
        fileManager: FileManager = .default,
        baseURL: URL = URL(fileURLWithPath: NSString(string: "~/.budget").expandingTildeInPath),
        decoder: JSONDecoder = JSONDecoder(),
        encoder: JSONEncoder = JSONEncoder()
    ) {
        self.fileManager = fileManager
        self.baseURL = baseURL
        self.decoder = decoder
        self.encoder = encoder

        // Create the base directory if it doesn't exist
        if !fileManager.fileExists(atPath: baseURL.path) {
            do {
                try fileManager.createDirectory(at: baseURL, withIntermediateDirectories: true, attributes: nil)
            } catch {
                // Log error here if needed
                // In production, you might want to pass the error to the caller instead
            }
        }
        
        // Configure date encoding/decoding
        decoder.dateDecodingStrategy = .iso8601
        encoder.dateEncodingStrategy = .iso8601
    }
    
    private var transactionsFileURL: URL {
        baseURL.appendingPathComponent("transactions.json")
    }
    private var categoriesFileURL: URL {
        baseURL.appendingPathComponent("categories.json")
    }
    
    /// Initializes the data store by attempting to load data from disk.
    func initialize(completion: @escaping (Bool) -> Void) {
        do {
            try loadData()
            completion(true)
        } catch {
            // You might log error details here
            completion(false)
        }
    }
    
    func loadData() throws {
        let loadedTransactions: [Transaction] = try loadFile(
            at: transactionsFileURL, 
            defaultValue: []
        )
        transactions = loadedTransactions

        let loadedCategories: [Category] = try loadFile(
            at: categoriesFileURL, 
            defaultValue: []
        )
        categories = loadedCategories
    }
    
    func saveData() throws {
        try saveFile(transactions, to: transactionsFileURL)
        try saveFile(categories, to: categoriesFileURL)
    }
    
    private func loadFile<T: Decodable>(at url: URL, defaultValue: T) throws -> T {
        guard fileManager.fileExists(atPath: url.path) else {
            return defaultValue
        }
        let data = try Data(contentsOf: url)
        return try decoder.decode(T.self, from: data)
    }
    
    private func saveFile<T: Encodable>(_ value: T, to url: URL) throws {
        let data = try encoder.encode(value)
        try data.write(to: url)
    }
    
    // MARK: - Transaction Methods
    
    func addTransaction(_ transaction: Transaction) throws {
        transactions.append(transaction)
        try saveData()
    }
    
    func updateTransaction(_ transaction: Transaction) throws {
        guard let index = transactions.firstIndex(where: { $0.id == transaction.id }) else {
            return
        }
        transactions[index] = transaction
        try saveData()
    }
    
    func deleteTransaction(_ transaction: Transaction) throws {
        transactions.removeAll { $0.id == transaction.id }
        try saveData()
    }
    
    // MARK: - Category Methods
    
    func addCategory(_ category: Category) throws {
        categories.append(category)
        try saveData()
    }
    
    func updateCategory(_ category: Category) throws {
        guard let index = categories.firstIndex(where: { $0.id == category.id }) else {
            return
        }
        categories[index] = category
        try saveData()
    }
    
    func deleteCategory(_ category: Category) throws {
        categories.removeAll { $0.id == category.id }
        try saveData()
    }
}
