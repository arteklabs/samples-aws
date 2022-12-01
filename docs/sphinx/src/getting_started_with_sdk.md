# About

The guide shows how to use the AWS SDK for JS (V3) with Typescript.

# Read The Docs

The [AWS SDK JS V3 API](https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/index.html) lists **AWS service clients**. Each of them has a corresponding npm package that needs to be installed individually. For example, the **AWS S3 service** has the corresponding npm client [@aws-sdk/client-s3](https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/clients/client-s3/index.html).

Reading through the documentation of the client, there is a list of **commands** that the client requests of the corresponding AWS service's API. Let's take as an example the **create-bucket** API endpoint and the corresponding npm client command [CreateBucketCommand](https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/clients/client-s3/classes/createbucketcommand.html). The documentation for the command/request specifies the **request parameters** [CreateBucketCommandInput](https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/clients/client-s3/interfaces/createbucketcommandinput.html) and the request's **response type** [CreateBucketCommandOutput](https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/clients/client-s3/interfaces/createbucketcommandoutput.html).

Reading through the documentation of each of these commands, there is a descriptive list of **properties**, that is, the **command's parameters**. For example, the `CreateBucketCommandInput` command specifies the parameter `Bucket` as **required** and the parameter `CreateBucketCommandInput` has **optional**, meaning that initializing the command requires that a parameter `Bucket` be specified.

The examples in **Service Client Authentication** and **Service Client API Request** will help you understand the above explanation. Mind however that an API request is a deferred asynchronous operation, meaning the developer must handle this complexity. The Python AWS SDK offers full transparency, but the JS V3 AWS SDK requires that the developer handles some of the complexity.

Start by learning about `Promises` and the `async/await` pattern in **In Promises We Trust**.

# In Promises We Trust

JS makes deferred asynchronous operations transparent with ``Promises``. Promises can be handled with the `async/await` pattern. Example:

```javascript
// function returns a promise because it's async
async function request(respTime) {

  // promise callback
  const callback = (resolve, reject) => {
    if (respTime < 500) {
      setTimeout(() => resolve('waiting time: acceptable'), respTime);
    } else {
      reject('waiting time: non-acceptable');
    }
  }

  // simulate a request with a response time respTime
  const promise = new Promise(callback);

  // wait asynchronously to resolve/reject the request response
  await promise.then(console.log).catch(console.log);
}


const time = 401;

request(time)

// however there's a call to request before a call to setTimeout, setTimeout 
// will execute first. That is because request returns a promise (that it
// handles itself)
setTimeout(() => console.log('impatiently awaiting...'), time - 1);

// impatiently awaiting...
// waiting time: acceptable
```

In regards to the SDK, executing `send` on a client returns a `Promise<ClientRequestOutput>`, meaning that instead of creating a new promise, we call the `send` method on the client object. The method encapsulates the callback logic, leaving us to handle the response either if the request is **fulfilled**, or if the request is **rejected**. The examples in **Service Client API Request** illustrate this.

# Authenticating A Service Client

After authenticating with the AWS account as described [here](aws_profile_authenticate.md), the SDK is able to read the temporary credentials and authenticate with the AWS account. The example below authenticates an S3 SDK client with the AWS profile:

```typescript
// import the commands and the required AWS Services package clients, and run
// the command using the .send method using the async/await pattern.
import { S3Client } from '@aws-sdk/client-s3';
import { fromIni } from '@aws-sdk/credential-providers';

const profile: string = '<your-profile>';
const region = '<your-region>';
const bucket: string = '<your-bucket-name>';

// make sure you've sso logged in with <your-profile> and moved the creds to
// '~/.aws/credentials' by running `npm run cpsso -- --profile <profile>`
const credentials = fromIni({ profile });

const s3 = new S3Client({
  credentials,
  region,
});
```

The example below authenticates an STS SDK client with the AWS profile:

```typescript
import {
  STSClient, STSClientConfig
} from '@aws-sdk/client-sts';

// assuming the same setup as described in the example above
const configuration: STSClientConfig = {
  credentials,
  region,
};
const sts: STSClient = new STSClient(configuration);
```



# Handling A Service Client API Request

The example below sends an API request to create an S3 bucket:

```typescript
// assuming the SDK has authenticated with a profile (see the section above)
import { CreateBucketCommand } from '@aws-sdk/client-s3';

async function request(){
  await s3.send(new CreateBucketCommand({ Bucket: bucket })).then((res) => {
    console.log('Success', res.Location);
  }).catch((err) => {
    console.log('Error', err);
  });
};

request();
```

The example below sends an API request to get information on the identity authenticating with the AWS profile:

```typescript
// assuming the SDK has authenticated with a profile (see the section above)
import {
  GetCallerIdentityCommand, GetCallerIdentityCommandInput
} from '@aws-sdk/client-sts';

async function request() {
  const input: GetCallerIdentityCommandInput = {};
  let command: GetCallerIdentityCommand;
  command = new GetCallerIdentityCommand(input);
  const res = await sts.send(command);
  return res;
}

request().then((res) => {
  console.log('Success');
  console.log(res.Account);
  console.log(res.UserId);
  console.log(res.Arn);
}).catch((err) => {
  console.log('Error');
  console.log(err);
});

// Success
// <profile-account-id>
// <hash>:<user-email>
// arn:aws:sts::<profile-account-id>:assumed-role/AWSReservedSSO_<role-name>_<hash>/<user-email>
```

# Resources

+ [AWS SDK for JS V3 - API Reference](https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/index.html)
+ [Configuring the SDK](https://docs.aws.amazon.com/sdk-for-javascript/v3/developer-guide/configuring-the-jssdk.html)
+ JS Promise and async/await pattern
  + [ms](https://developer.mozilla.org/fr/docs/Web/JavaScript/Reference/Global_Objects/Promise)
  + [web.dev](https://web.dev/promises/?gclid=CjwKCAjw2rmWBhB4EiwAiJ0mtcT4bn06OAhU3A1PfJ8YBAMi8X_I8hG7RlOh7VGzJOejTT2H8EcVOhoCzqcQAvD_BwE)
  + [javascript.info](https://javascript.info/async-await#:~:text=The%20await%20keyword%20before%20a,Otherwise%2C%20it%20returns%20the%20result.)