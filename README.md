# SmartContractsDecoderAuditor

Smart Contracts are essentially _Contracts written in Programming Languages like Solidity with various terms_ 
In future, with the advent of blockchain, NFTs, metaverse, cryptocurrencies etc., smart contracts are going to be the future. Various companies are coming up with new kinds of use cases of these smart contracts like SmartRealty is coming up with use in Real Estate Sector. CitiGroup recently launched a scheme for obtaining loans using these Smart Contracts.

But Lawyers are UNABLE to utilize these contracts or find it difficult to work with these contracts mainly because of being unversed with Programming languages. 
A tool to aid lawyers unversed in Programming of Smart Contracts. This app uses **EtherScan**, **PolygonScan** and **Verbwire APIs** to retrieve SmartContracts Data and then using **OpenAI API** to convert the Solidity Programming Code and Functions of the Smart Contracts into Plain English Legal Contractual Language comprehensible by Lawyers and Auditors.

**Features:**
1. **Convert Smart Contract to Plain English Legal Contract:** This is done by first obtaining the code, functions and other information from the EtherScan, PolygonScan and VerbWire APIs and then inputting running a query into the OpenAI API. The ChatGPT Model needs to be still **fine-tuned** on various existing smart contracts to obtain the perfect results.
   
3. **Ownership Checks with Contractual Checks**: When we buy a property or a bank keeps a mortgage on a property, it usually runs Tranfer Ownership Checks or CERSAI Checks to obtain relevant ownership information or information about any kind of encumbrances from the registry. This app will help the Buyers of NFT, Crypto or any other blockchain based product running on a Smart Contract to see if the ownership is in place and also for banks or other people indulged in lending to see the ownership is in the hands of the person applying for loan or mortgaging the assets.
