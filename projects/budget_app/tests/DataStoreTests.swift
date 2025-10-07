import XCTest
@testable import BudgetAppLib

@MainActor
final class DataStoreTests: XCTestCase {
    var dataStore: DataStore!
    var tempDirectory: URL!
    
    override func setUp() {
        super.setUp()
        // Use a unique subdirectory of the system temp directory
        tempDirectory = FileManager.default.temporaryDirectory
            .appendingPathComponent(UUID().uuidString)
        try? FileManager.default.createDirectory(at: tempDirectory, withIntermediateDirectories: true)
        
        // Pass your tempDirectory as baseURL to DataStore
        dataStore = DataStore(
            fileManager: FileManager.default,
            baseURL: tempDirectory
        )
    }
    
    override func tearDown() {
        try? FileManager.default.removeItem(at: tempDirectory)
        super.tearDown()
    }
    
    func testAddTransaction() async throws {
        let transaction = Transaction(
            title: "Test",
            amount: 100.0,
            date: Date(),
            category: "Food",
            type: .expense
        )
        
        try await dataStore.addTransaction(transaction)
        
        XCTAssertEqual(
            dataStore.transactions.count, 
            1, 
            "Expected exactly 1 transaction after adding one, but found \(dataStore.transactions.count)"
        )
        XCTAssertEqual(
            dataStore.transactions.first?.title, 
            "Test", 
            "Expected newly added transaction to have title \"Test\""
        )
    }
    
    func testAddCategory() async throws {
        let category = Category(name: "Food", subcategories: ["Groceries", "Restaurants"])
        try await dataStore.addCategory(category)
        
        XCTAssertEqual(
            dataStore.categories.count, 
            1, 
            "Expected exactly 1 category after adding one, but found \(dataStore.categories.count)"
        )
        XCTAssertEqual(
            dataStore.categories.first?.name, 
            "Food", 
            "Expected newly added category to have name \"Food\""
        )
    }
}
